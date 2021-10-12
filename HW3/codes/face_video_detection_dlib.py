import cv2
import dlib

def detect_faces(img):
    # 使用默认的人脸识别器模型
    detector = dlib.get_frontal_face_detector()
    # 图像预处理
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 人脸检测
    dets = detector(gray, 1)
    result = []
    for face in dets:
        x = face.left()
        y = face.top()
        x_with_w = face.right()
        y_with_h = face.bottom()
        result.append((x, y, x_with_w - x, y_with_h - y))
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
    detect_video('test2.mp4')