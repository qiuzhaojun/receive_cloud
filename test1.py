import cv2
cap = cv2.VideoCapture("rtsp://admin:XTExte123@10.157.115.207:9102/h264/ch1/sub/av_stream")
ret,frame = cap.read()
while ret:
    ret,frame = cap.read()
    cv2.imshow("frame",frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()
cap.release()