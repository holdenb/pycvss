import os
import random
import statistics		
import time
from pathlib import Path
import pycvss.utils as utils


"""
MIT License
Copyright (c) 2018 JP Janssen
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
"""

# NOTE A lot of this code is refactored from:
# https://github.com/Jpja/FFmpeg-Detect-Copy-Motion/blob/master/fdcm.py


###############################################################################
# TODO Refactor this code so the Fdcm is a lot simpler to understand. Also add
# functionality to take multiple input files as per original implementation.
# Possibly implement parallelism with multi file processing.
class Fdcm:
    """ FFmpeg Detect & Copy Motion (FDCM) dector object.
    FFmpeg Detect & Copy Motion (FDCM) automatically detects motion in video files.
    Each video motion event is saved to a new, separate video file. It works on most
    videos with a fixed camera angle and (almost) motionless background.

    FDCM is optimized for speed. A 1080p video should be processed 3-5x faster than
    the duration of the input file.

    The extracted files are lossless copies from the input file bitstream.
    """
    # basic parameters
    before_s = 1.2 #2.5              #start copying video N seconds before motion is triggered
    after_s = 1.2 #2                 #end copying video N seconds after motion has ended
    min_copy_break_s = 1.2 #5.9      #don't stop copying if next motion trigger sooner than this
    ignore_start_s = 1 #2           #seconds don't search for motion in beginning of input file
    ignore_end_s = 1 #2            #seconds don't search for motion at end of input file
    generate_output_file = True #set to False if you only want to read logs
    delete_input_file = False   #DANGEROUS, use only if you have COPIES of input files

    # out file parameters
    out_prefix = ''             #begin output filename with this
    out_from_in_start = 2       #substring of input file name. Large number copies entire filename
    out_from_in_end = 0         #substring of end of input file name
    out_random_letters = 1      #amount of random letters to add to output files. Same letters for all.
    out_counter_digits = 2      #least digits to counter. 2 means _01, _02, _03 etc
    out_lower_case = True       #force lower case filename
    out_delimiter = ''          #e.g. '-' to make filename more readable

    # cmd window log
    print_scores = False        #whether to print frame info (including scene scores)
    ffmpeg_loglevel = 31        #see https://ffmpeg.org/ffmpeg.html#Generic-options

    # advanced filter parameters
    step_len_f = 20 #20             #compare every n frame
    min_threshold_score = 0.0095 #0.0095 #default threshold. a score above indicates motion
    test_duration_s = 7 #7         #seek for a ('motionless'ish') segment this long. threshold automatically adjusts up if necessary (and possible)
    max_threshold_score = 0.04
    segments_smooth = 0         #assign median score from n segments before and after to smooth out scores
    segments_to_start = 2       #this many segments in a row above threshold triggers motion start
    segments_to_end = 6 #10        #this many segments in a row below threshold triggers motion end

    def __init__(self):
        self._input_file = None
        self._output_dir = None

    @property
    def input_file(self) -> str:
        return self._input_file

    @input_file.setter
    def input_file(self, input_: str):
        _file = Path(input_)
        if _file.exists() and not _file.is_file():
            raise FileNotFoundError(f'Invalid file: {input_}')

        name_parts = _file.name.split('.')
        if len(name_parts) == 2 and name_parts[1].upper() in utils.FILE_FORMATS:
            self._input_file = input_
        else:
            raise Exception('Invalid file format.')

    @property
    def output_dir(self) -> str:
        return self._output_dir

    @output_dir.setter
    def output_dir(self, output_) -> None:
        self._output_dir = output_

    def output_file_extension(self) -> str:
        """Get the output file extension

        Raises:
            Exception: If the input file does not exist

        Returns:
            str -- A string containing the file extension
        """
        if self._input_file is None:
            raise Exception("Invalid input file.")

        (_, file_extension) = os.path.splitext(self._input_file)

        return file_extension

    def process(self) -> None:
        """Process the input using the FDCM motion capture algorithm
        """
        t_0 = time.time()
        print(f'Processing: {self.input_file}')

        #get scenescores from ffmpeg
        # ffmpeg's scene change detection algo:
        # https://www.luckydinosaur.com/u/ffmpeg-scene-change-Fdcm

        # writes to a txt file, parse it into lists, then delete file
        randint = random.randint(10000, 99999)
        temp_file = "temp-scenescores-" + str(randint) + ".txt"

        if os.path.isfile(temp_file):
            os.remove(temp_file)

        command = "ffmpeg -loglevel " \
            + str(self.ffmpeg_loglevel) \
            + " -i \"" \
            + self.input_file \
            + "\" -vf select='not(mod(n\," \
            + str(self.step_len_f) \
            + "))',select='gte(scene,0)',metadata=print:file=" \
            + temp_file \
            + " -an -f null -"

        print('Run command: ' + command)
        os.system(command)

        f = list()
        f_pts = list()
        f_pts_time = list()
        f_scene_score = list()

        with open(temp_file) as file:
            text = file.read()

        i = -1
        while True:
            i = text.find('frame', i+1)
            if i == -1:
                break
            i = text.find(':', i) + 1
            j = text.find(' ', i)
            f.append(int(text[i:j]))
            i = text.find('pts', i+1)
            i = text.find(':', i) + 1
            j = text.find(' ', i)
            f_pts.append(int(text[i:j]))
            i = text.find('pts_time', i+1)
            i = text.find(':', i) + 1
            j = text.find('\n', i)
            f_pts_time.append(float(text[i:j]))
            i = text.find('scene_score', i+1)
            i = text.find('=', i) + 1
            j = text.find('\n', i)
            f_scene_score.append(float(text[i:j]))
        os.remove(temp_file)

        # give each frame a median score from +/- N frames
        f_median_score = list()

        for x in f:
            f_median_score.append(
                statistics.median(
                    f_scene_score[max(0, x-self.segments_smooth): x + self.segments_smooth+1]))

        #try to increase threshold if no motionless period found
        file_threshold_score = self.min_threshold_score

        while True:
            longest_motionless_s = 0
            last_change_s = 0
            run_s = 0
            for x in f:
                if f_median_score[x] < file_threshold_score:
                    run_s = f_pts_time[x] - last_change_s
                else:
                    if longest_motionless_s < run_s:
                        longest_motionless_s = run_s
                    last_change_s = f_pts_time[x]
            if longest_motionless_s <= self.test_duration_s:
                file_threshold_score += self.min_threshold_score
                if file_threshold_score > self.max_threshold_score:
                    file_threshold_score = self.min_threshold_score
                    break
            else:
                break

        # frame's score indicates CHANGE or not [0,1]
        f_change = list()
        for x in f:
            if f_median_score[x] >= file_threshold_score:
                f_change.append(1)
            else:
                f_change.append(0)

        # frame's TRIGGER score [-1,0,+1]
        f_trigger = list()
        x_max = len(f) - max(self.segments_to_start, self.segments_to_end)

        for x in f:
            if x >= x_max:
                f_trigger.append(0)
                continue
            run_above = 0
            for y in range(self.segments_to_start):
                if f_median_score[x + y] > file_threshold_score:
                    run_above += 1
            if run_above == self.segments_to_start:
                f_trigger.append(1)
            else:
                run_above = 0
                for y in range(self.segments_to_end):
                    if f_median_score[x + y] > file_threshold_score:
                        run_above += 1
                if run_above == 0:
                    f_trigger.append(-1)
                else:
                    f_trigger.append(0)

        # based on trigger scores, select "smart" COPY start and end points [-1,0,+1]
        f_copy = list()
        is_copying = 0
        end_time_s = f_pts_time[len(f) - 1]
        for x in f:
            f_copy.append(0)
            if f_pts_time[x] < self.ignore_start_s:
                continue
            if x >= x_max or f_pts_time[x] > end_time_s - self.ignore_end_s:
                if is_copying == 1:
                    # copy_end_s.append(f_pts_time[x])
                    f_copy[x] = -1
                continue

            # start copy?
            if is_copying == 0:
                # near end, don't make new starting point
                if f_pts_time[x] > end_time_s - self.ignore_end_s:
                    continue
                if f_trigger[x] == 1:
                    # copy_start_s.append(f_pts_time[x])
                    f_copy[x] = 1
                    is_copying = 1
                    continue

            # end copy?
            if is_copying == 1:
                if f_trigger[x] == -1:
                    can_end = 1
                    y = x
                    while True:
                        y += 1
                        if y >= x_max:
                            break
                        if f_trigger[y] == 1:
                            can_end = 0
                            break
                        if f_pts_time[y] - f_pts_time[x] > self.min_copy_break_s:
                            break
                    if can_end == 1:
                        #copy_end_s.append(f_pts_time[x])
                        f_copy[x] = -1
                        is_copying = 0
                    continue

        # set copy start and end times
        copy_start_s = list()
        copy_end_s = list()
        for x in f:
            if f_copy[x] == 1:
                copy_start_s.append(f_pts_time[x])
            if f_copy[x] == -1:
                copy_end_s.append(f_pts_time[x])	            

        # adjust start and end times
        for x, _ in enumerate(copy_start_s):
            copy_start_s[x] = max(copy_start_s[x] - self.before_s, 0)
            copy_end_s[x] = min(copy_end_s[x] + self.after_s, end_time_s)

        # print output values
        if self.print_scores:
            print('*')
            print("Frame;Time;Score;Median;Change;Trigger;Copy")
            for x in f:
                print(str(f[x]) + ";" + '%.4f' % (f_pts_time[x]) + ";"
                      + '%.4f' % (f_scene_score[x]) + ";" + '%.4f'%(f_median_score[x])
                      + ";" + str(f_change[x]) + ";" + str(f_trigger[x]) + ';' + str(f_copy[x]))

            print(self.input_file)

        print("Threshold: " + str(file_threshold_score))
        print('Copied clips: ' + str(len(copy_start_s)))

        if not copy_start_s:
            print('Nr;Start;End;Duration')
            for x, _ in enumerate(copy_start_s):
                print(str(x+1) + ';' + '%.2f' % (copy_start_s[x])
                      + ';' + '%.2f' % (copy_end_s[x]) + ';'
                      + '%.2f'%(copy_end_s[x] - copy_start_s[x]))

        #copy each motion segment as new file
        # stream is copied; no re-encoding or loss in quality
        in_filename, file_extension = os.path.splitext(self.input_file)
        file_num = 0

        #prepare random characters in output file name
        out_random = ''
        for i in range(self.out_random_letters):
            out_random += random.choice("abcdefghijkmnopqrstuvwxyz")

        # Create output directory if one has been set
        if self._output_dir is not None:
            if not os.path.exists(self._output_dir):
                os.makedirs(self._output_dir)

        path_prefix = self._output_dir if self._output_dir is not None else ''

        for x, _ in enumerate(copy_start_s):
            while True:
                file_num += 1
                out_filename = path_prefix + os.sep
                out_filename += str(file_num).zfill(self.out_counter_digits)
                out_filename += file_extension
                if self.out_lower_case:
                    out_filename = out_filename.lower()
                if os.path.isfile(out_filename) is False:
                    break

            clip_length = copy_end_s[x] - copy_start_s[x]

            command = 'ffmpeg -loglevel ' \
                + str(self.ffmpeg_loglevel) \
                + ' -ss ' \
                + '%.4f' % (copy_start_s[x]) \
                + ' -i \"' \
                + self.input_file \
                + '\" -t ' \
                + '%.4f' % (clip_length) \
                + ' -c copy \"' \
                + out_filename+'\"'

            print('Run command: ' + command)

            if self.generate_output_file:
                os.system(command)

        # delete input file?
        if self.delete_input_file:
            os.remove(self.input_file)

        #print time it took to process file
        t_1 = time.time()
        process_s = t_1-t_0
        times_faster = end_time_s / process_s

        print('File processed in '
              + '%.1f' % (process_s)
              + 's ('
              + '%.1f' % (times_faster)
              + 'x)')
