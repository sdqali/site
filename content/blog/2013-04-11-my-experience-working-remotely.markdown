---
bbissueid: 2
categories:
- development
- work
- learn
- reflections
comments: true
date: 2013-04-11
ghissueid: 59
image: /images/threaded-blue-on-black-cropped.jpg
tags:
- development
- work
- learn
- reflections
title: My experience working remotely
---

There has been a lot of debate in the tech community about working remotely and the willingness of employers to allow this option to their employees. At the very beginning of my career as a programmer, I had the opportunity to work on a distributed team. While the team was distributed, I was still working from an office and for almost half of the duration of my work on the team I had team members sitting beside me in the same office. Because of this, my scenario may not be representative of the population of programmers who work remotely. However, there are a number of things I learned from the experience that I would like to share.


# The Team
I was part of a four developer team, three of whom including me were co-located at the [ThoughtWorks](http://www.thoughtworks.com/) office in Bangalore. Our lead developer worked out of his house in the United Kingdom. While he had a great deal of experience writing software, the other team members had 1 year experience. This was the first ever team I was going to be part of and possibly the place where I would pick up important skills and learn a lot. We were writing mostly Ruby and JavaScript.

# The schedule
Our day would start with the three of us in Bangalore splitting in to a pair and a lone developer and working on code. The other developer would join around 9:00 AM GMT (~ 2:30 PM IST) and the lone developer would pair with him. Later, as the work day ended in India, the lead developer would continue to work till his day was over.

# Communication
We would have a short (~5 minutes) Skype call at the beginning of the UK work day, where we would discuss our progress and any thing else that needed to be shared. We later moved this to the end of the India work day, because this ensured the developers in India could discuss pressing matters and blockers with the lead developer and come back with this context the following day. We always had a private I.R.C. channel running where we could jump in and discuss things.

# The tools
While pairing remotely, we almost always used Emacs running in the no-window mode inside a [GNU screen](http://www.gnu.org/software/screen/) session. This was great as it was a fast and glitch-free experience. Coding in an IDE and sharing the desktop was too slow. This is where I picked up my Emacs skills. While pairing, we were constantly on a Skype call talking to each other. Being glued to the computer screen for hiurs while talking to somebody over Skype with an earphone plugged in to ears can be a tiring experience. Fortunately, we made sure to take sufficient breaks in between.
We used ThoughtWorks' [Mingle](http://www.thoughtworks-studios.com/mingle-agile-project-management) as our project management tool and card wall and it proved to be really useful for us.

# Sane practices
We were writing a client side JavaScript application and we were spending most of our time in an SSH session. How did we manage to make sure that things were not breaking? We did have to open up the application in our browsers to see how things got rendered and ensure that the UI workflow we were creating did not break. There are three things that helped us here. While none of these are specific to working remotely, these made life easy for us.
## Good code design
We took great efforts to encapsulate and structure our JavaScript code in to an [MVC](http://en.wikipedia.org/wiki/Model%E2%80%93view%E2%80%93controller). This enabled us to focus on and test individual parts of the application while making sure that the rest of the application would not break.

## Extensive unit tests
We wrote extensive unit tests for our JavaScript code. This kept our code working while evolving.

## Headless JS tests
We used [Rhino](https://developer.mozilla.org/en-US/docs/Rhino) to run JavaScript tests headlessly. This meant that we could run our tests from our terminals, while both developers looked at the results without having to bring up a browser.

None of these were done because we were a distributed team, it was the way we used to work.

# Mentoring
It was great to have more experienced developers to work alongside in the same room as you. I got to pair with them and ask questions if I was unable to grasp something. However during the latter half of my work as part of the team, it was just me and the senior developer from U.K. While he took great effort to mentor me, the time difference made it harder for me because for the first half of my work day, I was coding alone and did not have some body experienced to ask questions.

In conclusion, I would say that with the right people and the right tools, you can make remote work a good experience for your team. However, if there is someone that needs to be mentored, having the mentor co-located would be a great advantage.