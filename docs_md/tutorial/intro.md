<script async src="https://cdn.jsdelivr.net/npm/mathjax@2/MathJax.js?config=TeX-AMS-MML_CHTML"></script>

# Introduction

This tutorial will guide you through the essentials of hemlock. By the end of it, you'll be able to initialize hemlock projects, create powerful experiments and surveys, and deploy them on the web.

## Start with the end product in mind

When learning to program - or anything else - start with the end product in mind. This is my spin-off of Covey's *start with the end in mind*, where the end is something you've produced rather than knowledge you've acquired. I personally find that aiming at a product makes me more knowledgable about a topic than aiming at knowledge itself.

In this spirit, our goal is to create a behavioral study in which participants play an *ultimatum game* with each other in real time. You can see the end product here: <a href="https://hemlock-tutorial.herokuapp.com/" target="_blank">https://hemlock-tutorial.herokuapp.com/</a>. The <a href="https://github.com/dsbowen/hemlock-tutorial/blob/v0.11/survey.py" target="_blank">complete survey code is on github</a>.

The ultimatum game is famous; studied in hundreds of academic papers in disciplines such as game theory, behavioral economics, experimental economics, marketing, psychology, sociology, and neuroscience. It involves two players; a *proposer* and a *responder*. We begin by endowing the proposer with a 'pot' of (usually) money, e.g. $20. The proposer then proposes a 'split' of the pot between him/herself and the responder (e.g. *I get $15, you get $5*). The responder can accept or reject the proposed split. If the responder accepts, the pot is split according to the proposal (e.g. proposer gets $15, responder gets $5). If the responder rejects the proposal, both players get nothing.

With nearly 2000 citations, <a href="https://www.jstor.org/stable/2006907" target="_blank">this 1991 American Economic Review paper</a> studies how play evolves over successive rounds. It finds that proposers usually make 'fair' offers (about a 50-50 split), and responders usually reject unfair offers, in early rounds. As the game continues, proposers make more unfair offers, and responders are more accepting of them. The study we'll make in the hemlock tutorial is designed to replicate this finding.

## Prerequisites

This tutorial assumes a very basic knowledge of two programming languages: bash and python.

#### Tutorials

There are a thousand excellent 'bash/python for beginners' tutorials online. The following should teach you enough bash and python to get started with hemlock in about 1-2 hours. 

- Read up to 'Viewing Files' in [this bash tutorial](https://towardsdatascience.com/basics-of-bash-for-beginners-92e53a4c117a). 
- Complete up to Lesson 15 in [code the blocks](https://codetheblocks.com/).
- Learn how dictionaries work in [thinkcspy](https://runestone.academy/runestone/books/published/thinkcspy/Dictionaries/intro-Dictionaries.html).

#### What to do if something doesn't make sense

If and when you run into something which doesn't make sense to you, try the following:

1. **Keep going.** As best you can, press on with the tutorial. You don't have to 100% understand what's going on to get things working. You'll also find that things which don't make sense now often 'fall into place' just a short while later.
2. **Look it up.** I've done my best to write a clear, thorough tutorial. But no tutorial is comprehensive. If you run into something so puzzling that you can't just keep going, look it up! The internet is inundated with great programming resources.

<!-- ## For game theorists: a note on equilibrium concepts

This note is irrelevant to the hemlock tutorial; it's mostly to appease the game theorists in the audience.

We may object to the description of 'fair' versus 'unfair' offers; preferring to discuss equilibrium and non-equilibrium strategies. I'll take a moment to discuss equilibrium strategies and outcomes assuming that a player's utility is monotonically increasing in his/her own payoff and is independent of other players' payoffs.

In the classical ultimatum game in which the proposer has a continuous action space, there are multiple Nash equilibria, but a unique subgame perfect Nash equilibrium (SPNE). The SPNE strategies are that the proposer offers $0 and the responder will accept any offer, meaning that the SPNE outcome is that the proposer will receive the entire pot and the responder will receive $0.

Our game modifies the classical ultimatum game in two respects. First, the proposer has a discrete action space. Offers are in increments of $1. This opens up a second SPNE strategy set: the proposer offers $1 and the responder accepts any offer except for $0, meaning that the SPNE outcome is that the proposer will receive the entire pot minus $1 and the responder will receive $1.

The second and more important modification is that players move simultaneously, rather than sequentially. Rather than receiving an offer then accepting or rejecting it, responders announce a number such that they will accept any offer which gives them at least that amount of money. To predict gameplay, consider trembling hand perfect equilibria (THPE). The THPE strategy sets and outcomes are similar to the SPNE strategy sets and outcomes:

1. The proposer offers $0 with probability \(1-(|A_p|-1)\epsilon\), where \(A_p\) is the proposer's action set, and offers all other amounts with probability \(\epsilon\). The responder announces $0 with probability \(1-(|A_r|-1)\epsilon\), where \(A_r\) is the responder's action set, and announces all other amounts with probability \(\epsilon\). The modal equilibrium outcome is that the proposer receives the entire pot and the responder receives $0.
2. The proposer offers $1 with probability \(1-(|A_p|-1)\epsilon\), and offers all other amounts with probability \(\epsilon\). The responder announces $1 with probability \(1-(|A_r|-1)\epsilon\), and all other amounts with probability \(\epsilon\). The modal equilibrium outcome is that the proposer receives the entire pot minus $1 and the responder receives $1. -->