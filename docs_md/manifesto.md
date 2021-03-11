<!-- 
The 3 day challenge
Philosophy: simple things easy; complex things possible
Graph: simple, intermediate, complex
    Most research today is intermediate: Andreas example
Learning curve graph
Graph: Arc of technical progress in science
    Freud to R
    Low-hanging fruit is scarce
    The parable of Paul
Objections:
    Better things to do with your time
    If I can do it in Qualtrics, I should do it in Qualtrics
        Example of the html tables
    You can insert your own javascript in Qualtrics
Welcome to the 21st century
 -->

# Why Hemlock?

**I invented Hemlock to increase the speed and quality of social science research.**

During the first year of my Ph.D., I spent hundreds of hours creating behavioral experiments in Qualtrics. I remember the tediousness of copying and pasting blocks of questions, the struggle of implementing branching logic, and the frustration of updating hundreds of nearly-identical questions whenever my advisor wanted to modify the phrasing.

My experience wasn't unique. Every social science Ph.D. student, research assistant, and professor spends hundreds of hours, year after year, mired in a monotonous struggle with a GUI that looks like it was downloaded from a bootlegged floppy disk.

Throughout my Ph.D., I've worked with dozens of intelligent, hard-working colleagues, research assistants, and professors. They have better things to do with their time than shuffle question blocks or implement conditional logic using a drop-down menu. So do you. Qualtrics is an unacceptable waste of your time. Hemlock is the solution.

Another lesson I learned as a first-year Ph.D. student is that most social science research today is dull and useless. Social science researchers picked 98% of the low-hanging fruit between 1970 and 1990. Because there's almost nothing left on the lowest branches, it takes a combination of exceptional skill and luck to discover something new and worthwhile.

Why don't we reach beyond the lowest branches of our discipline? The answer, in part, is antiquated technology. It breaks my heart to see my colleagues imagine an exciting research idea, only to dilute it beyond recognition so they can implement it in Qualtrics. If the technology you're using limits your imagination and ambition, you need to use better technology. Hemlock is the solution.

## The 3 day challenge

**Set aside three days to learn python and Hemlock. Expect to struggle but resolve to push through.**

In March 2019, I was sitting at my computer, furiously hacking away at the next great Hemlock feature. Next door, I heard my colleague talking to Qualtrics support, trying to implement a new survey design. She had spent the last two days on the phone with Qualtrics, desperately trying to fix what should have been a simple problem.

I knocked on her door and asked what she was trying to do. In 10 minutes, I coded her survey as specified and sent her a link. She was excited.

"How did you do that?" she asked. I invited her to my computer and proudly displayed my python file. "Ugh, I have to learn how to code?" she said audibly, then walked away and redialed Qualtrics support.

Coding is scary. I get it. As an undergrad, I retook computer science 101 three times because I failed it twice and gave up majoring in computer science as a Sophomore. But I decided to overcome my fear of coding as a Ph.D. student because I was tired of Qualtrics wasting my time and stifling my imagination.

If you're an intermediate-level programmer (e.g., comfortable with R, new to python), I estimate it will take you three full days to learn the basics of python and Hemlock. Three days sounds like a long time. But if you set aside the time now and put in the effort, Hemlock will save you hundreds of hours throughout your career and enable you to shatter boundaries in your field.

<!-- ## Hemlock saves you time

A few weeks ago, my colleague from Cornell and I are shooting the breeze. He tells me his collaborator made a study that required some relatively simple (but still too complicated for Qualtrics) loop logic. So, the collaborator spent a full 40-hour work week copying and pasting blocks and adding convoluted branching logic in the Qualtrics GUI and QSF.

I like a good challenge, so I tell my colleague to simply describe the study to me verbally start a timer. 1 hour and 13 minutes later, I email him a link to the Hemlock version.

Let's imagine an alternative universe where my colleague's collaborator decides to use Hemlock instead of Qualtrics. Let's say it takes him 4 full days (32 hours) to learn basic python and the Hemlock package. And let's say, because he's new to Hemlock, that it takes him 4 times as long as it took me to make his study (5 hours). In this alternative universe, the collaborator learns python and Hemlock, makes his study, and still has 3 hours left over to kick back and sip mojitos.

Here's a rough back-of-the-envelope calculation. Suppose, conservatively, you spend an average of 1 day a week making studies in Qualtrics for 5 years - e.g. as a PhD student - for a total of 2,000 hours. Now suppose you learn Hemlock, which (again, conservatively) speeds up the process by an average of 25%. That's a time savings of 500 hours.

I'm guessing you're a researcher at a selective university, which means you're among the luckiest and brightest people in the world. Your time is valuable, and what you do matters. Copying and pasting blocks in a GUI that looks like it was downloaded from a dusted-off floppy disk is an unacceptable waste of your time and effort.

## Hemlock allows you to shatter boundaries

## The arc of technical progress

## There is no more low-hanging fruit

Let me address an ostensible contraditiction: 

## Common objections

#### If I *can* do it it Qualtrics, I *will* do it in Qualtrics -->

<!-- It's time for the big unveiling. I've been working on Hemlock for the last 6 months - largely from a remote village in Guatemala - and I'm finally ready to demo my shiny, beautiful new software. I send out an invite to the whole department and book the conference room for not one but two time slots to accommodate my audience.

I put on my best shirt, throw open the door at precisely 12 noon and... the conference room is empty. No problem; I'm sure there'll be an extra large crowd for the second time slot. I take my lunch, tuck my shirt back in, throw open the door at precisely 1PM and... my three favorite colleagues are eagerly awaiting my demo. Score. -->

<!-- I'm giving a Hemlock demo in my department when one of my colleagues asks, *Can you give me an example of when I would want to use Hemlock instead of Qualtrics?*. 

No problem. Prof. Bob Axelrod from Michigan is running forecasting studies in which participants predict AI players' actions in a game theoretic setting. He's got the python code written to simulate the AI players. The players play a game, and after each of 40 rounds, the participant predicts what the players will do next. But it's not integrated into the survey. So, he displays the game in a terminal window, which looks something like this:

```
Player 1: ['Defect', 'Defect', 'Cooperate', 'Cooperate', 'Defect', 'Cooperate', 'Cooperate', 'Defect', 'Cooperate', 'Defect'] Player 2: ['Cooperate', 'Cooperate', 'Defect', 'Defect', 'Cooperate', 'Defect', 'Cooperate', 'Cooperate', 'Cooperate', 'Cooperate']
```

Participants have to go back and forth between entering things into the terminal window and entering things in Qualtrics to keep the python simulation synchronized with Qualtrics. (And, by the way, because participants have to use a terminal window, you can't distribute the study online).

But now imagine you're using Hemlock. You've already got the python code to run the simulation, so all you need is one line of code to put the results a table. Problem solved!

*Okay, but you could still do something like this in Qualtrics,* my colleagues say. *For one thing, you could run (let's say) 20 different games, write code to translate each round of each game into an HTML table, and copy and paste each table into Qualtrics. Another idea: you could write python code to write out QSF code.*

Let's take these suggestions one at a time. First, my colleague suggests running 20 games, 40 rounds each (that's 800 tables), copying and pasting them one by one into a corresponding 800 Qualtrics pages, then writing the branching logic to randomly assign participants to observe one of the 20 games. And what happens when you want to run a variation of this study? Copy and paste another 800 HTML tables?

Second, my colleague suggests writing python code to write QSF code. But then, why not just use Hemlock and write python code? That's like saying you should first write your paper in Norwegian and then translate it into English instead of just writing it in English to begin with.

This reaction is an example of a common objection: *If I* can *do it in Qualtrics, I* will *do it in Qualtrics.* Sure, maybe it's not literally impossible to do your research in Qualtrics. But is it *easier* to do your research in Qualtrics? Put differently, which scares you more: spending 3 days learning python and Hemlock, or copying and pasting dozens of blocks and hundreds of HTML tables for study after study in paper after paper for your entire career? -->