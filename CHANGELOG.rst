Changelog
=========

v2.0.1 (2019-09-03)
-------------------
- Prevent pushing when replaying data. [pierre-louis.k]
- Catch IO exceptions. [pierre-louis.k]

v2.0.0 (2019-04-17)
------------
- Harmonize display of computed parameters. [pierre-louis.k]
- Change stdev percentile from 95 to 97 for binarize threshold
  estimation [BaptistePotier]
- Add print for auto computed values. [BaptistePotier]
- Add camera height parameters. [BaptistePotier]
- Remove unused parameters, hide fixed ones and update default values.
  [BaptistePotier]
- Put detection area in config. [pierre-louis.k]
- Add line edit mode. [pierre-louis.k]

  Press e to enter edit mode
  Click to add point, ctrl + click to remove last one 
- Add manual counting. [pierre-louis.k]

  Press i to add 1 in
  Press o to add 1 out
- Add trajectory visualization. [pierre-louis.k]
- Implements multi-segment counter. [pierre-louis.k]
- Update Trackers architecture to support multiple event listeners.
  [pierre-louis.k]
- Clean import sections, encoding and shebang. [pierre-louis.k]
- Add documentation. [pierre-louis.k]
- Remove and clean unused part of the code [pierre-louis.k]
- Add service install commands and files. [pierre-louis.k]


v1.4.0 (2018-11-07)
------------
- Split fps estimation into separate class. [pierre-louis.k]
- Add version number in config sample. [pierre-louis.k]
- Change kernel size for better noise reduction. [BaptistePotier]
- Check for each previous contour if new minimum is within. [pierre-
  louis.k]
- Add check if former local minimum is within new contour. [pierre-
  louis.k]
- Fix tracking id reset. [pierre-louis.k]
- Pack all shared variables in a common dictionary. [pierre-louis.k]
- Implement lighter version of head detection. [pierre-louis.k]
- Add shared variables for auto-config. [pierre-louis.k]
- Move tracker type to "fixed_param" section [pierre-louis.k]
- Add parameters calculations. [BaptistePotier]
- Separate config params in 3 categories. [BaptistePotier]
- Add parameters for bilateral filter, moving average. Separate the
  background params from counting params. [BaptistePotier]
- Add moving average and bilateral filtering. [BaptistePotier]
- Add bilateral filter. [BaptistePotier]
- Add std deviation computation per pixel. [BaptistePotier]
- Add refactored detectors skeletons. [pierre-louis.k]
- Fix age coloring and rectangle thickness. [pierre-louis.k]
- Refactor tracking with strategy pattern. [pierre-louis.k]


v1.3.1 (2018-08-28)
-------------------
- Fix program not resetting or resetting two times at start. [pierre-
  louis.k]


v1.3.0 (2018-08-24)
-------------------
- Catch first reset call. [pierre-louis.k]
- Disable waitKey() call when no active window. [pierre-louis.k]
- Set GET request timeout to 10 sec. [pierre-louis.k]
- Add frame by frame mechanism. [pierre-louis.k]
- Add pausing mechanism. [pierre-louis.k]
- Add IOError exception handling in file reader. [pierre-louis.k]
- Adapt reset hour mechanism to accommodate config reload. [pierre-
  louis.k]
- Add reload on reset_hour and "r" key press. [pierre-louis.k]
- Put windows name as constants. [pierre-louis.k]
- Add proper person ID reset. [pierre-louis.k]
- Fix bug when (background - threshold) is negative (roll-over) [pierre-
  louis.k]
- Update default parameters. [pierre-louis.k]
- Change unit of max tracking distance to pixel. [pierre-louis.k]
- Add tracker type parameter. [pierre-louis.k]
- Add playback rate to command line argument. [pierre-louis.k]

  Default is 30 fps
- Add maximum tracking age as parameter in config file. [pierre-louis.k]
- Color untracked people in red. [pierre-louis.k]
- Sort partnerships by person id to become more deterministic. [pierre-
  louis.k]
- Look for minimal distance in case of conflicts. [pierre-louis.k]
- Reduce rectangle thickness. [pierre-louis.k]
- Add new tracking function. [pierre-louis.k]

  Add max tracking distance parameter
- Add windows move on first frame. [pierre-louis.k]
- Add key polling behaviour and frame wait timeout. [pierre-louis.k]

  Escape key press now terminate the program
- Add stop boolean to FileReaderProcess. [pierre-louis.k]
- Add  gitchangelog configuration file and changelog file. [pierre-
  louis.k]


v1.2.3 (2018-07-12)
-------------------
- Fix computation of remaining pixels to detect. [pierre-louis.k]


v1.2.2 (2018-07-11)
-------------------
- Add fps display. [pierre-louis.k]
- Record on person on end of tracking up to a maximum buffer size.
  [pierre-louis.k]
- Clean RingBuffer. [pierre-louis.k]
- Add matching bounding rectangle ratio. [BaptistePotier]


v1.2.1 (2018-07-10)
-------------------
- Change size of matching people to rectangle. [BaptistePotier]
- Merge branch 'pre-release' into feature/refactor_tracking.
  [BaptistePotier]


v1.2.0 (2018-07-10)
-------------------
- Remove unnecessary import. [pierre-louis.k]
- Disable dynamic background by default. [pierre-louis.k]
- Correct sample config file. [pierre-louis.k]

  Typo in param name
  Add reset_hour param
- Correct way of computing remaining pixels. [pierre-louis.k]
- Clean Person class. [pierre-louis.k]
- Switch to 2-point crossing. [pierre-louis.k]
- Fix 3-point line crossing. [pierre-louis.k]
- Fix frame number not increasing when middle pixel is not checked.
  [pierre-louis.k]
- Add unique counter for one id. [BaptistePotier]
- Clean tracking function and Person class. [pierre-louis.k]

  Remove unnecessary functions and variables
  Rename variables
- Add colour to visualization. [pierre-louis.k]
- Clean code and add comments. [pierre-louis.k]
- Limit camera values to max range. [pierre-louis.k]
- Remove scaling from driver. [pierre-louis.k]
- Reject max range when increasing background. [pierre-louis.k]

  This avoid updating background with wrong values with fast moving objects
- Add disable option for dynamic background. [pierre-louis.k]

  To disable it set bg_frame_interval to 0 or less
- Enhance dynamic background. [pierre-louis.k]

  Add decay rate parameter
  Compensate rates with frame interval
  Reject zeros when decreasing background
- Add parameter for binarize threshold. [pierre-louis.k]
- Fix indentation issue. [pierre-louis.k]
- Fix typo. [pierre-louis.k]
- Remove cast and fix missing frame number increase. [pierre-louis.k]
- Add dynamic background parameters and comments. [pierre-louis.k]
- Remove comments. [BaptistePotier]
- Tweak parameters. [BaptistePotier]
- Smoothen background subtraction. [BaptistePotier]


v1.1.4 (2018-07-09)
-------------------
- Correct way of computing remaining pixels. [pierre-louis.k]


v1.1.3 (2018-07-01)
-------------------
- Add reset_hour in config param. [pierre-louis.k]
- Add reset hour mechanism. [pierre-louis.k]
- Fix too much reversing. [pierre-louis.k]

  Now the variable for the count in is called cnt_in and the one for the count out is called cnt_out


v1.1.2 (2018-06-21)
-------------------
- Fix redundancy. [pierre-louis.k]
- Fix version not displaying after cython. [pierre-louis.k]
- Make version printing future-proof. [pierre-louis.k]


v1.1.1 (2018-06-21)
-------------------
- Put version number inside MultiplePeopleCounter module. [pierre-
  louis.k]
- Make negative fps_window values disable fps computation. [pierre-
  louis.k]
- Fix frame skip in fps estimation. [pierre-louis.k]

  Fix typo as well
- Allow disabling fps computation by setting fps_window to 0. [pierre-
  louis.k]
- Set fps window of driver with value of counter. [pierre-louis.k]


v1.1.0 (2018-06-19)
-------------------
- Change txt logging to csv. [pierre-louis.k]
- Add more specific exception handling for data pushing. [pierre-
  louis.k]
- Change pushed data and add sensor_id param. [pierre-louis.k]
- Implement shared Boolean in Evo process. [pierre-louis.k]
- Add start script and driver process shared cancel Boolean. [pierre-
  louis.k]
- Fix beep count and closing. [pierre-louis.k]


v1.0.0 (2018-06-12)
-------------------
- Bump version: 0.0.0 → 1.0.0. [pierre-louis.k]
- Add bumpversion config file and version string in main.py. [pierre-
  louis.k]
- Fix cython compile script. [pierre-louis.k]
- Merge branch 'fix/rename_camera_driver' into test/cython. [pierre-
  louis.k]
- Change driver name. [pierre-louis.k]
- Merge branch 'test/bits_removal' into test/cython. [pierre-louis.k]
- Correctly exit while statement in corner cases to avoid infinite loop.
  [pierre-louis.k]
- Merge branch 'feature/config_file' into test/bits_removal. [pierre-
  louis.k]
- Add safer parameter mapping. [pierre-louis.k]
- Correct lambda parameters naming. [pierre-louis.k]
- Decrease kernel size of binarization and inflate contours. [pierre-
  louis.k]
- Add bit_square_size param to config. [pierre-louis.k]
- Clean code. [pierre-louis.k]
- Add bit removal and new end of search condition. [pierre-louis.k]
- Fix naming typo. [pierre-louis.k]
- Fix tuple access. [pierre-louis.k]
- Remove prints. [pierre-louis.k]
- Merge branch 'test/cython' into feature/config_file. [pierre-louis.k]
- Add .so files to gitignore. [pierre-louis.k]
- Add MultiplePeopleCounterConfig to cython compile file. [pierre-
  louis.k]
- Merge branch 'feature/config_file' into test/cython. [pierre-louis.k]
- Refactor detection to set max tracked objects. [pierre-louis.k]
- Rename lambda. [pierre-louis.k]
- Merge branch 'test/cython' into feature/config_file. [pierre-louis.k]
- Remove so file from code versionning. [pierre-louis.k]
- Add entry point. [pierre-louis.k]
- Correct file reader process for compilation. [pierre-louis.k]
- Ignore build files. [pierre-louis.k]
- Add cython compilation script. [pierre-louis.k]
- Replace erode by two close. [BaptistePotier]
- Change parameters findcontour. [BaptistePotier]
- Change parameters for testing. [BaptistePotier]
- Put threshold above background. [pierre-louis.k]

  Remove averaged pixel around close range shapes
- Erode foreground to remove noise. [pierre-louis.k]
- Inflate detected before slicing. [pierre-louis.k]
- Fix draw contour to mask. [pierre-louis.k]
- Reset slice every time. [pierre-louis.k]
- Find contours on a copy of masked_foreground. [pierre-louis.k]
- Enhance detection to iteratively search for person. [pierre-louis.k]
- Change all zeros to max not only where binarized is zero. [pierre-
  louis.k]
- Merge branch 'feature/config_file' into test/detection_flicker.
  [pierre-louis.k]
- Add debug prints in head detection. [pierre-louis.k]
- Put lambda as parameter of map_config_param function. [pierre-louis.k]
- Add safe recursive getters-setters to ConfigSection. [pierre-louis.k]
- Wrap config file in Object to allow dotted access. [pierre-louis.k]
- Merge branch 'feature/push_data' into feature/config_file. [pierre-
  louis.k]
- Add asynchronous data pushing. [pierre-louis.k]
- Specify GPIO buzzer as not implemented. [pierre-louis.k]
- Add recursive function to print config dictionary. [pierre-louis.k]
- Merge branch 'feature/enhance_event_logging' into feature/config_file.
  [pierre-louis.k]
- Change write mode to append. [pierre-louis.k]
- Add counter reset on day change. [pierre-louis.k]
- Rewrite event logging. [pierre-louis.k]
- Merge branch 'feature/config_file' [pierre-louis.k]
- Add parameters from config file for upper and lower tracking limits.
  [pierre-louis.k]
- Merge branch 'feature/config_file' into 'master' [Kabaradjian PL]

  Feature/config file

  See merge request terabee_applications/iot/people_counting_depth_cam!2
- Update sample yaml. [pierre-louis.k]
- Add loading logging parameters from config file. [pierre-louis.k]
- Add flipping and rotate parameters from config (no real effect yet)
  [pierre-louis.k]
- Add data pushing from config file. [pierre-louis.k]
- Merge branch 'feature/enhance_tracking' into feature/config_file.
  [pierre-louis.k]
- Check for the same id that it cannot cross two time in or out.
  [BaptistePotier]
- Add param from config to reverse counting logic. [pierre-louis.k]

  Create separate count_in and count_out function
- Add param from config for frames recording. [pierre-louis.k]

  Clean prints in counter
- Catch exception when config file is not found. [pierre-louis.k]
- Add buzzer config. [pierre-louis.k]
- Add middle pixel check config. [pierre-louis.k]
- Add window display config parameters. [pierre-louis.k]
- Rename "main" window to "visualization" [pierre-louis.k]
- Enhance driver prints. [pierre-louis.k]

  Prefix with [Driver] and more information
- Add config file reading for counting_params. [pierre-louis.k]
- Rename config as sample and exclude yaml from cvs. [pierre-louis.k]
- Add sample config file. [pierre-louis.k]
- Move buzzer test file to miscs. [pierre-louis.k]
- Print less fps indication and replace value, change thickness of
  middle line. [BaptistePotier]
- Merge branch 'feature/raspberrypi3' [pierre-louis.k]
- Enhance binarize zero rejection speed. [ub2-64]
- Disable middle pixel sanity check. [pierre-louis.k]
- Reject 0 when binarizing. [pierre-louis.k]
- Replace sum par np.sum. [BaptistePotier]
- Background recalculation for sun. [BaptistePotier]
- Create raspberry pi 3 branch for testing arm sdk. [BaptistePotier]
- Add prints for background computation status. [pierre-louis.k]
- Reduce number of fps prints. [pierre-louis.k]
- Tune buzzer parameters. [ub1-64]
- Add buzzer to counting class. [pierre-louis.k]
- Add PwmBuzzer class file. [pierre-louis.k]
- Merge branch 'feature/evo_trigger_process' into feature/buzzer.
  [pierre-louis.k]
- Change recording event in counter. [pierre-louis.k]
- Add evo serial process. [pierre-louis.k]
- Move main to people_counting_depth_cam.py. [pierre-louis.k]
- Merge branch 'feature/refactor' into feature/rework_recording.
  [pierre-louis.k]
- Rename counter file. [pierre-louis.k]
- Move unused files to miscs directory. [pierre-louis.k]
- Merge branch 'feature/multithreading' into feature/refactor. [pierre-
  louis.k]
- Change path of saved files. [pierre-louis.k]
- Add asynchronous buffer saving. [pierre-louis.k]
- Add playback from one file. [pierre-louis.k]

  Now the camera driver or the file reader will wait for the array to be copied by the counter before overwritting the buffer with a new frame
- Create buzzer file. [BaptistePotier]
- Fix naming typos. [pierre-louis.k]
- Add filre reader process class skeleton. [pierre-louis.k]
- Rename driver process class to DriverProcess. [pierre-louis.k]

  Change "thread" to "process"
- Add and clean member variables. [pierre-louis.k]
- Add .npy and .npz to .gitignore. [pierre-louis.k]
- Record ring_buffer and background on detection. [pierre-louis.k]

  Move ring buffer from driver to process
- Change some methods to static. [pierre-louis.k]

  Fix non-existent membre variables
- Add argument handling and usage display in main. [pierre-louis.k]
- Rename shut_down to shutdown. [pierre-louis.k]
- Add wrapper for middel pixel function. [pierre-louis.k]
- Change flag to event and put background generation inside driver
  process. [pierre-louis.k]
- Rework ring buffer. [pierre-louis.k]
- Clean variables name. [pierre-louis.k]
- Merge branch 'black_magic_test' into 'feature/multithreading'
  [Kabaradjian PL]

  Black magic test

  See merge request terabee_applications/iot/people_counting_depth_cam!1
- Remove old for loops. [pierre-louis.k]
- Get map faster. [pierre-louis.k]
- Synchronize Counter and Driver. [pierre-louis.k]
- Add FPS computation in driver. [pierre-louis.k]
- Merge branch 'feature/refactor' into feature/multithreading. [pierre-
  louis.k]
- Rename main class. [pierre-louis.k]
- Merge branch 'feature/multithreading' into feature/refactor. [pierre-
  louis.k]
- Merge branch 'feature/refactor' into feature/multithreading. [pierre-
  louis.k]
- Add comments for tracking part. [BaptistePotier]
- Correct text position. [Aggelina Chatziagapi]
- Change array dimensions for wide door setup. [pierre-louis.k]
- Clean code. [pierre-louis.k]
- Add shared flag for device readiness. [pierre-louis.k]
- Add shared array between process. [pierre-louis.k]
- Merge remote-tracking branch 'origin/feature/multithreading' into
  feature/multithreading. [pierre-louis.k]
- Print frame, suppress print len queue. [BaptistePotier]
- Suppress the useless print. [BaptistePotier]
- Put driver object in run() [pierre-louis.k]
- Rename thread to process. [pierre-louis.k]
- Add multiprocessing queues. [pierre-louis.k]

  Not working still
- Add multithreading class. [pierre-louis.k]
- Merge branch 'feature/refactor' [pierre-louis.k]
- Clean tracking function. [pierre-louis.k]
- Add fps count. [pierre-louis.k]
- Copy array before detecting contours. [pierre-louis.k]
- Add self in front of threshold detection and put 2 iterations for the
  cv2 open. [BaptistePotier]
- Merge branch 'clean_repository' [pierre-louis.k]
- Merge branch 'feature/refactor' into clean_repository. [pierre-
  louis.k]
- Fix visualization update. [pierre-louis.k]

  Put detect threshold in object
  Change nb_bgrnd_frame from 20 to 60
- Correct binarization. [pierre-louis.k]
- Restructure code to centralize logic in run() [pierre-louis.k]
- Merge branch 'clean_repository' into feature/refactor. [pierre-
  louis.k]
- Correct filename. [pierre-louis.k]
- Replace tabs by 4 spaces. [pierre-louis.k]
- Remove comments. [pierre-louis.k]
- Change background subtractor, binarize and head detection function.
  [BaptistePotier]
- Merge remote-tracking branch 'origin/clean_repository' into
  feature/refactor. [BaptistePotier]
- Fix acronym in camel case. [pierre-louis.k]
- Rename npz concatenator. [pierre-louis.k]
- Rename person file. [pierre-louis.k]
- Rename ring buffer. [pierre-louis.k]
- Rename camera driver. [pierre-louis.k]
- Clean test.py. [pierre-louis.k]
- Merge branch 'feature/testing' [pierre-louis.k]
- Exclude archives from git. [pierre-louis.k]
- Add filename as script argument. [pierre-louis.k]
- Merge remote-tracking branch 'origin/feature/testing_live' into
  feature/testing. [pierre-louis.k]
- Add .gitignore. [pierre-louis.k]
- For testing. [Aggelina Chatziagapi]
- Adding README file. [Aggelina Chatziagapi]
- Adding README file. [Aggelina Chatziagapi]
- Correction to save the extra frames as well. [Aggelina Chatziagapi]
- Load videos and their continuation. [Aggelina Chatziagapi]
- Concatenate npz arrays. [Aggelina Chatziagapi]
- Add imshow. [Aggelina Chatziagapi]
- Small changes. [Aggelina Chatziagapi]
- Merge remote-tracking branch 'origin/feature/testing_live' [pierre-
  louis.k]
- Add output.txt to gitignore. [Aggelina Chatziagapi]
- Fix frame by frame recording. [Aggelina Chatziagapi]
- Add gitignore and clean repo. [Aggelina Chatziagapi]
- Correction. [Aggelina Chatziagapi]
- Shut down the camera. [Aggelina Chatziagapi]
- Check if camera initialization is correct. [Aggelina Chatziagapi]
- Ensure adding strings. [Aggelina Chatziagapi]
- Spaces correction. [Aggelina Chatziagapi]
- Write output to file. [Aggelina Chatziagapi]
- Print middle pixel depth for 1st and 2nd frame. [Aggelina Chatziagapi]
- Small changes. [Aggelina Chatziagapi]
- Concatenate the npz frames. [Aggelina Chatziagapi]
- Correction 2. [Aggelina Chatziagapi]
- Correction. [Aggelina Chatziagapi]
- Record while testing. [Aggelina Chatziagapi]
- Test on upboard. [Aggelina Chatziagapi]
- Some changes, while testing. [Aggelina Chatziagapi]
- Small changes. [Aggelina Chatziagapi]
- Accuracy 94.5% on 145 data. [Aggelina Chatziagapi]
- Testing on some gathered videos. [Aggelina Chatziagapi]
- Merge remote-tracking branch 'origin/feature/kris_testing' [pierre-
  louis.k]
- Add driver test file to display depth map. [Aggelina Chatziagapi]
- Merge remote-tracking branch 'origin/feature/recording' [pierre-
  louis.k]
- Small changes. [Aggelina Chatziagapi]
- Check correct init of camera & improve extra frames saving. [Aggelina
  Chatziagapi]
- Save the continuation. [Aggelina Chatziagapi]
- Try to add extra frames, if EVO is triggered again. [Aggelina
  Chatziagapi]
- Recording .npz per 1 minute. [Aggelina Chatziagapi]
- Recording corrections. [Aggelina Chatziagapi]
- Record main. [Aggelina Chatziagapi]
- Record numpy array until ^C. [Aggelina Chatziagapi]
- Resolved merge conflict. [Aggelina Chatziagapi]
- Changes on upboard for recording. [Aggelina Chatziagapi]
- Check if there is a previous triggering. [Aggelina Chatziagapi]
- Flush input for EVO. [Aggelina Chatziagapi]
- Recording when EVO is triggered, using PLK's functions for EVO.
  [Aggelina Chatziagapi]
- Recording using cyclic buffer. [Aggelina Chatziagapi]
- Merge remote-tracking branch 'origin/master' [pierre-louis.k]
- Small corrections. [Aggelina Chatziagapi]
- Adding the dataset url (Google Drive) [Aggelina Chatziagapi]
- Adding README file. [Aggelina Chatziagapi]
- Add gitignore. [pierre-louis.k]
- Initial commit. [Aggelina Chatziagapi]
- Initial commit. [Aggelina Chatziagapi]
