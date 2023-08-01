import subprocess
import multiprocessing
import coreography
import time
import sys
import os
import music_detection as md
import glob, os
import pydub
import signal
import platform


def playSong(song, dur):
    if sys.platform.startswith('linux'):
        os.chdir('..')
        bashCommand = "play " + song
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
    elif sys.platform.startswith('win32'):
        import winsound
        os.chdir('..')
        song = os.path.join(os.getcwd(), song)
        winsound.PlaySound(song, winsound.SND_FILENAME)
    else:
        os.chdir('..')
        file_path=os.path.join(os.getcwd(), song)
        dur = 10
        os.system("afplay " + song)
#        os.system("sleep " + dur)
#        os.system("kill pgrep afplay")

#        file_path = os.path.join(os.getcwd(), song)
#        duration_ms = dur*1000  # Durata in millisecondi (5 secondi)
#        play_audio_with_duration(file_path, duration_ms)

#        song = os.path.join(os.getcwd(), song)
#        playSound(song)
#        bashCommand = "afplay " + song
#        os.system(bashCommand)
#        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
#        output, error = process.communicate()

def dance(moves, robot_ip, robot_port):
    print("Dance!")
    os.chdir('..')
    os.chdir('..')
    os.chdir(os.path.join(os.getcwd(), "NaoMoves"))
    
    for move in moves[0]:
        python2_command = f"python -m {move} {robot_ip} {robot_port}"
        process = subprocess.run(python2_command.split(), stdout=subprocess.PIPE)
        print("Move: {}".format(move), flush=True)

def main():
    robot_ip = input("Insert Robot IP: ")
    robot_port = input("Insert Robot Port: ")

    list_songs = []
    os.chdir(os.getcwd() + "/Music")
    print()
    print("AVAILABLE SONGS:")
    i=1
    for file in glob.glob("*.wav"):
        list_songs.append(file)
        print(i, ":", file)
        i+=1

    print()
    index = int(input("Which song would you like to play? Choose the number: "))
    print()
    song= list_songs[index -1]
    dur= int(input("Set the duration of the choreography (in seconds): "))
    print()
    print("You chose the song || " + song + " || NAO will dance for:  ", dur, " seconds!")

    # --------------------------------------------------------------# ADDED
    # Select a random song and analyze the amplitude
    #song = md.random_song()
    analyzed_song = md.analyze_music(song)
    # --------------------------------------------------------------# ADDED
    moves = coreography.search_coreography(analyzed_song, dur)
    process1 = multiprocessing.Process(target=playSong, args=(song, dur))

    process2 = multiprocessing.Process(target=dance, args=((moves,), robot_ip, robot_port))
    
    process1.start()
    process2.start()
    print(process1.pid)
    print(process2.pid)
#    process1.terminate()
#    process2.terminate()
# Aspetta che i processi terminino effettivamente
    process2.join()
#    process1.join()
#    process2.join()
    process1.terminate()


#    print(os.getpid())
#    bashCommand = "killall " + str(process1.pid)
#    bashCommand = "kill -9 " + os.getpid()
#    os.system(bashCommand)

    if process1.is_alive():
        print("alive p1")
        process1.kill()
    if process1.is_alive():
        print("still alive p1")
    else:
        print("NOT alive p1")
    if process2.is_alive():
        print("alive p2")
        process2.terminate()
    else:
        print("NOT alive p2")



if __name__ == '__main__':
    main()
