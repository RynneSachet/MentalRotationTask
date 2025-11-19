#this program displays 3 letters, mirrored and normal with 4 orientations. Participants are asked 
#to identify whether stimuli is mirrored or normal. Before each letter a fixation cross appears
#for 1 second, with suppression audio randomly playing or not. If audio plays during fixation,
#it continues through the letter. Data is printed at the end.
#Data Output: 
#   Letter, 
#   Suppression(True or False), 
#   Correct(whether answer was correct), 
#   ResponseTime in seconds

from psychopy import visual, core, event, sound
import random, csv

#create a window
win = visual.Window([800,600], monitor = "testMonitor", units = "pix", color = "white")

#Instruction screen
instructions = visual.TextStim(
    win,
    text="Press 'M' when shown a mirrored letter.\nPress 'Enter' when shown an unmirrored letter.\n\nPress any key to begin.",
    color="black",
    height=24,
    wrapWidth=700
)

#Draw instructions and wait for key
instructions.draw()
win.flip()
event.waitKeys()

#Stimulus dictionary
stimulus = {
    ("F", "normal"): "UM_F_0.jpg", ("F", "mirrored"): "M_F_0.jpg",
    ("G", "normal"): "UM_G_0.jpg", ("G", "mirrored"): "M_G_0.jpg",
    ("R", "normal"): "UM_R_0.jpg", ("R","mirrored"): "M_R_0.jpg"
}

#Stimulus image object
stim = visual.ImageStim(win, size = (300,300))

#Orientation options
orientations = [0, 45, 135, 180]

#Suppression audio
suppSound = sound.Sound("500_hrz.mp3", loops = -1)

#Fixation cross
fixation = visual.TextStim(win, text="+", color="black", height=40)

#results and rt clock
results = []
clock = core.Clock()

#All trials combined
trials = [
    (letter, version, orientation)
    for letter in ["F","R","G"]
    for version in ["normal", "mirrored"]
    for orientation in orientations
]

#Randomize order
random.shuffle(trials)

#Trial loop
for letter, version, orientation in trials:
    
    #random suppression selection
    supp = random.choice([True, False])

    #fixation period with suppression
    if supp:
        suppSound.play()
    else:
        suppSound.stop()
    
    fixation.draw()
    win.flip()
    core.wait(1.0)  #fixation lasts 1 second

    #letter presentation (audio continues if supp=True)
    stim.image = stimulus[(letter, version)]
    stim.ori = orientation

    stim.draw()
    win.flip()

    #measure RT
    clock.reset()
    keyPress, responseTime = event.waitKeys(
        keyList=["m", "return", "escape"], timeStamped = clock
    )[0]

    if keyPress == 'escape': #exit program if needed 
        win.close()
        core.quit()

    #correct response
    correct = (keyPress == 'm') if version == "mirrored" else (keyPress == 'return')
    
    #append trial results
    results.append([letter, supp, correct, responseTime])

    #stop audio (only after response)
    suppSound.stop()

#Exit screen
end_text = visual.TextStim(
    win,
    text="All trials completed.\nThank you!",
    color="black",
    height=24,
    wrapWidth=700
)

end_text.draw()
win.flip()
event.waitKeys()

#Print results
print(results)

#Save results to CSV
with open("guy_man_results.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Letter", "Suppression", "Correct", "ResponseTime"])
    writer.writerows(results)

#Close window
win.close()
core.quit()
