#
# Created by Berke Akyıldız on 14/June/2019
#
import sys

import cv2
import os


def processFrame(img, frame_width, frame_height, cur_minutes, cur_seconds, total_minutes, total_seconds, count, frame_count):
    font = cv2.FONT_HERSHEY_SIMPLEX
    bottomLeftCornerOfText = (500, frame_height - 5)
    fontScale = 1
    fontColor = (255, 255, 255)
    lineType = 2

    if total_seconds <= 9:
        t_seconds = "0" + str(total_seconds)
    else:
        t_seconds = str(total_seconds)

    if total_minutes <= 9:
        t_minutes = "0" + str(total_minutes)
    else:
        t_minutes = str(total_minutes)

    if cur_seconds <= 9:
        c_seconds = "0" + str(cur_seconds)
    else:
        c_seconds = str(cur_seconds)

    if cur_minutes <= 9:
        c_minutes = "0" + str(cur_minutes)
    else:
        c_minutes = str(cur_minutes)

    timestamp = c_minutes + ":" + c_seconds + " / " + t_minutes+ ":" + t_seconds
    framestamp = str(count) + " / " + str(frame_count)

    topRightCornerOfText = (frame_width - 250, 50)


    cv2.resize(img, (frame_width, frame_height))
    cv2.putText(img, timestamp,
                bottomLeftCornerOfText,
                font,
                fontScale,
                fontColor,
                lineType)
    cv2.putText(img, framestamp,
                topRightCornerOfText,
                font,
                fontScale,
                fontColor,
                lineType)
    cv2.imshow("image", img)
    # print(img.shape)


def writeFrame(count, img, fileName):
    outputPath = fileName + "_output\\"
    if not os.path.exists(outputPath):
        os.mkdir(outputPath)
    cv2.imwrite(outputPath + "frame%d.png" % count, img)
    print("Saved %d Frame" % count)


def calculateWaitTime(fps):
    return (1.0 / fps) * 1000


def getDuration(file):
    cap = cv2.VideoCapture(file)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    return int(frame_count / fps)


def getFPS(file):
    cap = cv2.VideoCapture(file)
    return cap.get(cv2.CAP_PROP_FPS)


def getFrames(file):
    cap = cv2.VideoCapture(file)
    return cap.get(cv2.CAP_PROP_FRAME_COUNT)


def writeAllFramesBetween(startFrame, endFrame, file):
    cap = cv2.VideoCapture(file)
    count = startFrame
    cap.set(1, startFrame)

    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            if count >= endFrame:
                break
            writeFrame(count, frame, os.path.basename(file))
            count += 1
        else:
            break

    cap.release()


def showInPlayer(file):
    cap = cv2.VideoCapture(file)

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    duration = getDuration(file)

    total_minutes = int(duration / 60)
    total_seconds = duration % 60
    print("fps: " + str(fps) + "\n")
    print("frame count: " + str(frame_count) + "\n")
    print("duration: " + str(total_minutes) + ":" + str(total_seconds))

    count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            key = int(calculateWaitTime(fps))
            wait = cv2.waitKey(key)
            cur_frame = cap.get(cv2.CAP_PROP_POS_FRAMES)
            cur_duration = int(cur_frame / fps)
            cur_minutes = int(cur_duration / 60)
            cur_seconds = cur_duration % 60

            processFrame(frame, frame_width, frame_height, cur_minutes, cur_seconds, total_minutes, total_seconds,
                         count, frame_count)
            count += 1

            if wait == ord('q'):
                break
            elif wait == ord('s'):
                writeFrame(count, frame, os.path.basename(file))
                print("pressed s")
        else:
            break

    cap.release()

    cv2.destroyAllWindows()


def main():
    help = "-m for showing in a media player\n-c for running in command line\n-a for writing all " \
           "frames\n"

    commandLineUsage = "COMMAND LINE USAGE    python player.py -c [start-second] [end-second] [FILE-PATH]\n"
    mediaPlayerUsage = "MEDIA PLAYER USAGE    python player.py -m [FILE-PATH]\nAfter video started, press 's' in keyboard to save current frame\n"
    allUsage = "WRITE ALL FRAMES USAGE     python player.py -a [FILE PATH]"
    usage = "USAGE:    python player.py [OPTIONS] [FILE-PATH]" + "\n" + help + commandLineUsage + mediaPlayerUsage + allUsage
    arguments = sys.argv
    try:
        prompt = arguments[1]
        if prompt == '-m':
            if arguments[2] in arguments:
                filePath = arguments[2]
                filePath.replace("\\", "\\\\")
                showInPlayer(filePath)
            else:
                print(mediaPlayerUsage)
        elif prompt == '-c':
            if arguments[4] in arguments:
                filePath = arguments[4]
                filePath.replace("\\", "\\\\")
                duration = getDuration(filePath)
                fps = getFPS(filePath)
            else:
                print("\nInclude file path.")
                print(commandLineUsage)
                sys.exit()
            if arguments[2] in arguments:
                startSecond = arguments[2]
            else:
                print("\nInclude start second number.")
                print(commandLineUsage)
                sys.exit()
            if arguments[3] in arguments:
                endSecond = arguments[3]
            else:
                print("\nInclude end second number.")
                print(commandLineUsage)
                sys.exit()
            startFrame = fps * int(startSecond)
            endFrame = fps * int(endSecond)

            writeAllFramesBetween(startFrame, endFrame, filePath)

        elif prompt == '-a':
            if arguments[2] in arguments:
                filePath = arguments[2]
                filePath.replace("\\", "\\\\")
                total_frames = getFrames(filePath)
                writeAllFramesBetween(0, total_frames, filePath)
            else:
                print(allUsage)
        elif prompt == '-h':
            print(usage)
            print(mediaPlayerUsage)
            print(commandLineUsage)

        else:
            print("No argument entered.")
            print(usage)
    except:
        print(usage)

if __name__== "__main__":
    main()
