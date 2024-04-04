# MediaPipe Hand Tracking

利用 MediaPipe 进行手部特征点追踪，当我的手部特征点出现在指定区域内时，程序作出回应。

假设椭圆白框是切割机（具体形状可调），当我的手部特征点在椭圆内时，视频图像上相应的关键点出现 WARNING 警告，同时程序终端里也给出左右两只手相应关键点的位置和是否存在警告。

![椭圆白框示例](https://github.com/hengsleep/MediaPipe-Hand-Tracking/assets/120698260/63f5b035-b3fb-42e9-b935-8f7f91738cbd)

原先还想在视频上显示出椭圆函数方程，却因此发现一个 OpenCV 的 bug。`putText` 函数里以 `img` 形式呈现的文本不允许存在特殊符号。有些字体可能不包含所有 Unicode 字符，导致无法正确显示。

![椭圆函数方程示例](https://github.com/hengsleep/MediaPipe-Hand-Tracking/assets/120698260/b0cb1c79-2e57-4bf2-96a8-d567f3535bc5)

Python 版本要求：`cv2`, `mediapipe`, `numpy`
