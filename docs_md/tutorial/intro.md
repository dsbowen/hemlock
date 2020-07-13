# Introduction

This tutorial will guide you through the essentials of hemlock. By the end of it, you'll be able to initialize hemlock projects, create powerful experiments and surveys, and deploy them on the web.

## Start with the end product in mind

When learning to program - or anything else - start with the end product in mind. This is my spin-off of Covey's *start with the end in mind*, where the end is something you've produced rather than knowledge you've acquired. I personally find that aiming at a product makes me more knowledgable about a topic than aiming at knowledge itself.

In this spirit, our goal is to create a behavioral study in which participants play an *ultimatum game* with each other in real time. You can see the end product here: <http://hemlock-tutorial.herokuapp.com/>. The complete survey code is here: <https://github.com/dsbowen/Hemlock/blob/master/survey.py>.

The ultimatum game is famous; studied in hundreds of academic papers in disciplines such as game theory, behavioral economics, experimental economics, marketing, psychology, sociology, and neuroscience. It involves two players; a *proposer* and a *responder*. We begin by endowing the proposer with a 'pot' of (usually) money, e.g. $20. The proposer then proposes a 'split' of the pot between him/herself and the responder (e.g. *I get $15, you get $5*). The responder can accept or reject the proposed split. If the responder accepts, the pot is split according to the proposal (e.g. proposer gets $15, responder gets $5). If the responder rejects the proposal, both players get nothing.

With nearly 2000 citations, [this 1991 American Economic Review paper](https://www.jstor.org/stable/2006907) studies how play evolves over successive rounds. It finds that proposers usually make 'fair' offers (about a 50-50 split), and responders usually reject unfair offers, in early rounds. As the game continues, proposers make more unfair offers, and responders are more accepting of them. The study we'll make in the hemlock tutorial is designed to replicate this finding.