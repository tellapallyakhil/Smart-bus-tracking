from deep_sort_realtime.deepsort_tracker import DeepSort

tracker=DeepSort(max_age=30)

def track_buses(detections,frame):
    tracks=tracker.update_tracks(detections,frame=frame)
    tracked_objects=[]

    for track in tracks:
        if not track.is_confirmed():
            continue
        track_id=track.track_id
        l,t,r,b=map(int,track.to_ltrb())
        tracked_objects.append((track_id,(l,t,r,b)))

    return tracked_objects
