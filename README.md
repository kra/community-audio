# comment collecting interface

- raspbian lite buster
- GeneralPlus usb sound
- storage drive mounted on /mnt/futel

## on pi:

run raspi-config

interfacing enable ssh

reboot

enable passwordless ssh to pi user

## local:

update deploy/hosts pibox for correct ip address

XXX uncomment sub-recipes in playbook.yml and run this repeatedly with each? In any case, get the whole process run.

ansible-playbook -i deploy/hosts playbook.yml

# on pi:

edit /usr/share/alsa/alsa.conf

defaults.ctl.card 1

defaults.pcm.card 1

append alsa.conf.part to /usr/share/alsa/alsa.conf

adjust levels with alsamixer

sudo crontab -e

# run and kill alsaloop once so it doesn't gum up for some reason

@reboot (alsaloop -C pcm.dsnoop -P plughw:1,0 -c 1 &) && (sleep 0.25) && killall -9 alsaloop

reboot

## usage:

boot

wait several minutes

user picks up handset to hear prompt and record message

admin retrieves and deletes collected wav files from /mnt/futel

## todo:

sync storage, allow turning off without saving?
- what does this mean?
audio plays after hookswitch has been down
- stop playing when hookswitch has been down for a bit
- avoid bounces, check periodically, resart if down for 2 periods?
limit recording length
- current is 10 mins?
error if left off hook for long period
- left off hook for 9 hours, no response after put on hook
- had to power cycle
- is this because audio file is being written or something?
- test to make sure this isn't an error for any period of long idle whether on hook or not

## notes:

drive capacity
- 5 megs per minute
- 200 mins per gig
- 6400 mins per 32GB drive

speaker volume
- root@raspberrypi:/mnt/futel# amixer -c 1 cset numid=6 75%

this has delay
- arecord --format S16_LE -c 2 -D hw:0 | aplay
