import cv2

def detect_faces(img):
    # 加载分类器
    face_cascade = cv2.CascadeClassifier('./haarcascades/haarcascade_frontalface_default.xml')
    # 图像预处理
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)
    # 人脸检测
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
    result = []
    for (x, y, w, h) in faces:
        result.append((x, y, w, h))
    return result


def draw_faces(img):
    faces = detect_faces(img)
    if faces:
        _id = 0
        for (x, y, w, h) in faces:
            _id += 1
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.rectangle(img, (x - 1, y - h // 5 - 2), (x + 1 + w, y), (0, 0, 255), -1)
            cv2.putText(img, "Person" + str(_id), (x + 2, y - h // 15), cv2.FONT_HERSHEY_TRIPLEX, (h / 150), (0, 255, 0), 1)
    return img


def detect_video(filename=""):
    # f = 0 实时检测人脸，否则从 MP4 文件中检测
    f = 0 if len(filename) <= 0 else filename

    # 打开视频捕获设备
    video_capture = cv2.VideoCapture(f)
    print(video_capture)

    # 设置检测后的输出文件参数
    width = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = 30
    out = cv2.VideoWriter('out.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

    while True:
        # 逐帧读取视频
        ret, frame = video_capture.read()
        # 人脸检测并绘制包围框
        new_frame = draw_faces(img=frame)
        # 显示视频
        cv2.imshow('VideoFaceDetect', new_frame)
        # 存储视频
        out.write(new_frame)
        # 退出
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # 关闭摄像头设备
    video_capture.release()
    # 关闭所有窗口
    cv2.destroyAllWindows()



if __name__ == "__main__":
    # detect_video()
    detect_video('test1.mp4')