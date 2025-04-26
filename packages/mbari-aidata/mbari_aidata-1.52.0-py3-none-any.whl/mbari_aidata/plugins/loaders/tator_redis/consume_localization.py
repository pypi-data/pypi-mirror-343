# mbari_aidata, Apache-2.0 license
# Filename: plugins/loaders/tator_redis/consume_localization.py
# Description: commands related to loading localization data from Redis
import time
import json
import redis

from mbari_aidata.plugins.loaders.tator.localization import gen_spec, load_bulk_boxes
from mbari_aidata.plugins.loaders.tator.attribute_utils import format_attributes
from mbari_aidata.logger import info, debug, err


class ConsumeLocalization:
    def __init__(self, r: redis.Redis, api, tator_project, box_type):
        self.r = r
        self.api = api
        self.tator_project = tator_project
        self.box_type = box_type
        # Create a dictionary of key/values from the box type attributes field name and dtype
        self.attribute_mapping = {a.name: {"type": a.dtype} for a in box_type.attribute_types}

    def consume(self):
        while True:
            info("Waiting for new localizations...")
            try:
                keys = self.r.keys("locs:*")
                for k in keys:
                    info(f"Checking for valid media load for {k}")
                    video_ref = k.decode("utf-8").split(":")[1]
                    load_key = self.r.keys(f"tator_ids_v:{video_ref}")
                    if len(load_key) == 1:
                        hash_data = self.r.hgetall(f"locs:{video_ref}")
                        objects = {
                            key.decode("utf-8"): json.loads(value.decode("utf-8")) for key, value in hash_data.items()
                        }

                        # Load them referencing the video by its load_id
                        info(f"Getting tator_id from {load_key[0]}")

                        # Check if the key exists
                        if self.r.exists(load_key[0], "tator_id"):
                            tator_id = self.r.hget(load_key[0], "tator_id_v").decode("utf-8")
                            if tator_id == 'None':
                                err(f"tator_id not found for {load_key[0]}")
                            else:
                                info(f"Loading {len(objects)} localization(s) for video ref {video_ref} load_id {tator_id}")

                                boxes = []
                                for b in objects:
                                    obj = objects[b]
                                    debug(obj)
                                    if 'label' in obj:
                                        label = obj['label']
                                    if 'Label' in obj:
                                        label = obj['Label']
                                    info(f"Formatting {obj}")
                                    attributes = format_attributes(obj, self.attribute_mapping)
                                    boxes.append(
                                        gen_spec(
                                            box=[obj["x1"], obj["y1"], obj["x2"], obj["y2"]],
                                            version_id=obj["version_id"],
                                            label=label,
                                            width=obj["width"],
                                            height=obj["height"],
                                            attributes=attributes,
                                            frame_number=obj["frame"],
                                            type_id=self.box_type.id,
                                            media_id=int(tator_id),
                                            project_id=self.tator_project.id,
                                        )
                                    )

                                load_bulk_boxes(self.tator_project.id, self.api, boxes)

                                # Remove them from the queue
                                for obj_id in objects:
                                    info(f"Removing localization {obj_id} from queue")
                                    self.r.hdel(f"locs:{video_ref}", obj_id)
            except Exception as e:
                info(f"Error: {e}")
                time.sleep(5)

            time.sleep(5)
