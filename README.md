# FlaskOverflow

Stack Overflow like using Flask :panda_face:

## Installation

Will see.. :)

## Usage

This is mainly developed for the sake of developing.
I need experince in creating Web Application with Python. So I decided to go with Flask due to its minimalism and extensibility.

## History (in Milestones)

1. **Working app, very basic functionality (Questions, Answers)**
	- [x] Working app with no Users at all.
	- [x] DB with `Questions`, `Answers` (connected).
	- [x] Question feed, newest on top.
	- [x] Page serving question by # and showing its answers, adding new answer.
	- [x] Links between the different pages, so it can be navigated.

1. **Still working app, wider functionality (adding Tags, Front end updates)**
	- [x] "Add question" -> show the form only if requested.
	- [ ] Tags functionality:
		- [x] DB update with a new `Tags` table.
		- [x] Adding tags for each question.
		- [x] Displaying tags in both views (question feed and question view).
		- [ ] Some validation..?
		- [x] Front end improvements.
	- [x] Refactor -> A strong necessity for wrapping the data in objects. Classes to be the main goal for M3.

1. **Nice and working app, easily extensible (adding classes)**
	- [ ] class Question: `id, title, text, answers=[...],tags=[...]`
	- [ ] Refactor the existing code to make it work with the Question object instead.
	- [ ] ...
	- [ ] ...