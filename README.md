# led-metrosign
Grabs metro arrival times (and other data) and displays them on an LED sign

#Description
This program uses a Raspberry PI, the WMATA Metro API and an LED sign (http://brightledsigns.com/programmable/indoor/bs-4x16-mini)
to create a metro signboard that displays the current train times for my station.  Currently the program is called repeatedly via Cron every 30 seconds (shellscript that calls it twice with a 30 second delay).

Currently, some Linux dependencies exist such as the subprocess module.

#Setup
You need to obtain a WMATA API key by registering as a developer at https://developer.wmata.com/.  Or you can use the demo API key.  After obtaining the LED sign and a Raspberry PI, the files downloaded to the PI.  The config.json contains my default settings they can be changed by running this command from the commandline:

```
python3 getmetro2.py -s
```

The program will ask for your station code, time to walk to the metro, if you want to change the API key and if you want it to run in simulated mode.

You can find a listing of the 3 character station codes in the spreadsheet at:
https://kurtraschke.com/2011/01/metrorail-station-codes

Simulated mode prints results to the console instead of sending them to the sign.

Once the files are in place and set up, type

```
crontab -e
```

and enter

```
* * * * * python3 getmetro2.py
```

This will refresh the sign every minute. You can also replace this with a call to a shell script that to call it more frequently.

#Other Features
A custom message may be added by adding

```
python3 getmetro2.py -a "Message Here"
```

Note that the message should be enclosed by quotation marks.

The configuration can be reset by typing:

```
python3 getmetro2.py -r
```

#Future Work
Remove the linux dependenies (Cron usage and subprocess Python library).  Make the program both usable on Linux and Windows.

Add in Bus information and/or the ability to switch between the two.

Improve handling of exceptions such as serial port communication and IOErrors

#Requirements
This requires the pyserial module.

#Acknowledgements
This uses the BrightLEDSigns Python API (the ledsign folder)
https://github.com/BrightLedSigns/pyledsign
Copyright (c) 2013 Kerry Schwab & Bright Signs All rights reserved.

This program is free software; you can redistribute it and/or modify it under the terms of the the FreeBSD License . You may obtain a copy of the full license at:

http://www.freebsd.org/copyright/freebsd-license.html

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met: * Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer. * Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution. * Neither the name of the nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
