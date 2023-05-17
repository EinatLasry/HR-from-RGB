import sys
import cv2
import numpy as np
import time
from imutils import face_utils
from face import Face_utilities
from signal import Signal_processing
import statistics
from sys import argv
import csv
from tabulate import tabulate
from termcolor import colored
import os
os.system('color')

def start(video_or_webcam, ROI_num, path_of_subject):
    bpms = []
    video = True
    if video_or_webcam == "video":
        video = False

    if video:
        cap = cv2.VideoCapture(0)
    else:
        cap = cv2.VideoCapture(path_of_subject)

    fu = Face_utilities()
    sp = Signal_processing()

    i = 0
    last_rects = None
    last_shape = None
    last_age = None
    last_gender = None
    face_detect_on = False
    age_gender_on = False

    t = time.time()

    # for signal_processing
    BUFFER_SIZE = 100

    fps = 0  # for real time capture
    video_fps = cap.get(cv2.CAP_PROP_FPS)  # for video capture
    print("Video FPS:", video_fps)
    times = []
    data_buffer = []
    # data for plotting
    filtered_data = []
    fft_of_interest = []
    freqs_of_interest = []
    bpm = 0

    while True:
        # grab a frame -> face detection -> crop the face -> 68 facial landmarks -> get mask from those landmarks
        # calculate time for each loop
        t0 = time.time()
        if (i % 1 == 0):
            face_detect_on = True
            if (i % 10 == 0):
                age_gender_on = True
            else:
                age_gender_on = False
        else:
            face_detect_on = False
        ret, frame = cap.read()
        if frame is None:
            cv2.destroyAllWindows()
            break

        ret_process = fu.no_age_gender_face_process(frame, "68")
        if ret_process is None:
            cv2.putText(frame, "No face detected", (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.imshow("frame", frame)

            cv2.destroyWindow("face")
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break
            continue
        rects, face, shape, aligned_face, aligned_shape = ret_process

        (x, y, w, h) = face_utils.rect_to_bb(rects[0])
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        if (len(aligned_shape) == 68):

            # Drawing ROI1 - Left Chick - YELLOW
            cv2.rectangle(aligned_face, (aligned_shape[54][0], aligned_shape[29][1]),
                          (aligned_shape[12][0], aligned_shape[33][1]), (0, 255, 255), 0)

            # Drawing ROI2 - Right Chick - GREEN
            cv2.rectangle(aligned_face, (aligned_shape[4][0], aligned_shape[29][1]),
                          (aligned_shape[48][0], aligned_shape[33][1]), (0, 255, 0), 0)

            # Drawing ROI3 - Forehead - BLUE
            distance = abs(shape[30][1] - shape[28][1])
            # [20][0]  [20][1]-distance   [25][0]    [20][1]
            cv2.rectangle(aligned_face, (aligned_shape[19][0], aligned_shape[20][1] - distance),
                          (aligned_shape[24][0], aligned_shape[20][1]), (255, 0, 0), 0)

            # Drawing ROI4 - Rectangle face - WHITE
            cv2.rectangle(aligned_face, (aligned_shape[3][0], aligned_shape[20][1] - distance),
                          (aligned_shape[15][0], aligned_shape[58][1]), (255, 255, 255), 0)

            new_shape = aligned_shape[:16, :]
            new_shape = np.append(new_shape, aligned_shape[26, :])
            new_shape = np.append(new_shape, aligned_shape[25, :])
            new_shape = np.append(new_shape, aligned_shape[24, :])
            new_shape = np.append(new_shape, aligned_shape[23, :])
            new_shape = np.append(new_shape, aligned_shape[22, :])
            new_shape = np.append(new_shape, aligned_shape[21, :])
            new_shape = np.append(new_shape, aligned_shape[20, :])
            new_shape = np.append(new_shape, aligned_shape[19, :])
            new_shape = np.append(new_shape, aligned_shape[18, :])
            new_shape = np.append(new_shape, aligned_shape[17, :])
            pts = np.array(new_shape, np.int32)
            pts = pts.reshape((-1, 1, 2))
            color = tuple(map(int, (255, 255, 0)))
            # Drawing ROI5 - Face Segmentation - CYAN
            cv2.polylines(aligned_face, [pts], True, color, 0)  # True if you want the closed shape

        else:
            cv2.rectangle(aligned_face, (aligned_shape[0][0], int((aligned_shape[4][1] + aligned_shape[2][1]) / 2)),
                          (aligned_shape[1][0], aligned_shape[4][1]), (0, 255, 0), 0)

            cv2.rectangle(aligned_face, (aligned_shape[2][0], int((aligned_shape[4][1] + aligned_shape[2][1]) / 2)),
                          (aligned_shape[3][0], aligned_shape[4][1]), (0, 255, 0), 0)

        for (x, y) in aligned_shape:
            cv2.circle(aligned_face, (x, y), 1, (0, 0, 255), -1)

        if ROI_num != "5":
            # for signal_processing
            ROIs = fu.ROI_extraction(aligned_face, aligned_shape, ROI_num)
            green_val = sp.extract_color(ROIs)
        else:
            maskkk = np.zeros(aligned_face.shape, np.uint8)
            out = np.zeros(aligned_face.shape, np.uint8)
            cv2.drawContours(maskkk, [pts], -1, (255, 255, 255), -1)
            out[maskkk == 255] = aligned_face[maskkk == 255]
            out = out[:, :, 1]
            green_val = out[out.nonzero()].mean()

        data_buffer.append(green_val)

        if (video == False):
            times.append(time.time() - t)
        else:
            times.append((1.0 / video_fps) * i)

        cv2.putText(frame, "Press 'q' to quit", (int(frame.shape[1] * 0.5), int(frame.shape[0] * 0.10)),
                    cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 0, 255), 2)

        L = len(data_buffer)

        if L > BUFFER_SIZE:
            data_buffer = data_buffer[-BUFFER_SIZE:]
            times = times[-BUFFER_SIZE:]
            # bpms = bpms[-BUFFER_SIZE//2:]
            L = BUFFER_SIZE
        if L == 100:
            fps = float(L) / (times[-1] - times[0])
            cv2.putText(frame, "fps: {0:.2f}".format(fps), (30, int(frame.shape[0] * 0.95)), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (255, 0, 0), 2)
            detrended_data = sp.signal_detrending(data_buffer)
            interpolated_data = sp.interpolation(detrended_data, times)
            normalized_data = sp.normalization(interpolated_data)
            fft_of_interest, freqs_of_interest = sp.fft(normalized_data, fps)
            max_arg = np.argmax(fft_of_interest)
            bpm = freqs_of_interest[max_arg]
            cv2.putText(frame, "HR: {0:.2f}".format(bpm), (int(frame.shape[1] * 0.6), int(frame.shape[0] * 0.95)),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            filtered_data = sp.butter_bandpass_filter(interpolated_data, (bpm - 20) / 60, (bpm + 20) / 60, fps, order=3)

        # write to txt file
        with open("a.txt", mode="a+") as f:
            f.write("time: {0:.4f} ".format(times[-1]) + ", HR: {0:.2f} ".format(bpm) + "\n")
            if bpm >= 48 and bpm <= 180:
                bpms.append(bpm)

        cv2.imshow("frame", frame)
        cv2.imshow("face", aligned_face)

        i = i + 1

        # waitKey to show the frame and break loop whenever 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            median, mean = calc(bpms)
            vector = [ROI_num, median, mean]
            headers = ["#ROI", "Median", "Mean"]
            print(colored(tabulate([vector], headers, tablefmt="pretty"), 'green'))
            sys.exit()

    cap.release()
    cv2.destroyAllWindows()
    median, mean = calc(bpms)
    vector = [ROI_num, median, mean]
    headers = ["#ROI", "Median", "Mean"]
    print(colored(tabulate([vector], headers, tablefmt="pretty"), 'green'))


def calc(bpms_array):
    try:
        median = statistics.median(bpms_array)
        median = "{:.2f}".format(median)
    except statistics.StatisticsError:
        median = float('NaN')
    try:
        mean = statistics.mean(bpms_array)
        mean = "{:.2f}".format(mean)
    except statistics.StatisticsError:
        mean = float('NaN')
    return median, mean


if __name__ == "__main__":
    video_or_webcam = argv[1]
    ROI_num = argv[2]
    if video_or_webcam.lower() == "video":
        path_of_subject = argv[3]
        start(video_or_webcam, str(ROI_num), path_of_subject)

    elif video_or_webcam.lower() == "webcam":
        start(video_or_webcam, str(ROI_num), "")
