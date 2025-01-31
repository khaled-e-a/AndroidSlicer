<img src="images/AndroidSlicer.png" width="250" height="250">


# AndroidSlicer
AndroidSlicer is a dynamic slicing tool for Android Apps, useful for a variety of tasks, from testing to debugging to security.

# Paper
[Dynamic Slicing for Android](https://dl.acm.org/citation.cfm?id=3339649)

Tanzirul Azim, Arash Alavi, Iulian Neamtiu, Rajiv Gupta. 

41st International Conference on Software Engineering (ICSE'19), May 2019.

# Usage
AndroidSlicer is in Java. You can find the source code under the "source" directory and the required scripts for running the tool under the "tool" directory.

1. After cloning/extracting the tool directory in a folder (e.g., ~/AndroidSlicer/tool), you just need to change the ***PLATFORDIRFORSLICER*** parameter in 3 **instrumenter.sh**, **preSlicer.sh**, and **AndroidSlicer.sh** script files. ***PLATFORDIRFORSLICER*** is the path of your android sdk/platforms folder.

2. Copy the app apk file that you want to do the slicing into the tool directory (i.e., ~/AndroidSlicer/tool/). 

3. Make sure that either your emulator is running or the phone is connected and accessible via adb. Then run the instrumenter script for the app using the following command:

   > **./instrumenter.sh <apk_file>**
   
   > [E.g., ./instrumenter.sh com.myapp.apk]

   This will instrument the app, sign the instrumented apk file, and install the app on your emulator/real phone.
   
   P.S. In order to instrument (or not instrument) specific classes of the app, you can uncomment line number 175 in *Instrumenter.java* and specify the specific classes that you want (or don't want) to be instrumented. Please note that it can potentially lead to missing dependencies, unless you are certain you won't miss dependencies by filtering out those classes. 
       
4. Run the following commands and then run the app on your emulator/real phone:

   >**adb logcat -c**

   >**adb logcat | grep SLICING > <apk_file>.logcat.txt**
   
   >[E.g., adb logcat | grep SLICING > com.myapp.apk.logcat.txt]

   After you finish with running the app, stop the above command. This will collect the required log file for AndroidSlicer.

5. Run the preSlicer script for the app:

   >**./preSlicer.sh <apk_file>**
   
   >[E.g., ./preSlicer.sh com.myapp.apk]

   This will create a <apk_file>.logcat.processed.txt file. Each line starts with a number. You need to pick a number (your interesting point as the slicing criteria) to add to the next command. 

6. Run the AndroidsSlicer script for the app and then enter the number that you picked from previous step:

   >**./AndroidsSlicer.sh <apk_file>**
   
   >[E.g., ./AndroidsSlicer.sh com.myapp.apk]
        
   Finally, you will have the slices files wrt your slicing criteria


# Contacts

If you have questions, please contact Arash Alavi: [aalav003@ucr.edu](aalav003@ucr.edu) or Tanzirul Azim: [tanzir.buet@gmail.com](tanzir.buet@gmail.com).
