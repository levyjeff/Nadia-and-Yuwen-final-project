# Data and Programming for Public Policy II
# PPHA 30536


## Final Project: Reproducible Research
## Autumn 2020


## Due: Sunday, December 6th by midnight on GitHub

## Author：Nadia Fitriani & Yuwen Xiong

## Results and Project explanation
Please check the [PDF file](Write up.pdf) for our findings and the detailed explanation of the project

## Coding Structure
1. [Web scraping, downloading, merging and tidying data](downloading_and_webscraping.py)
2. [Data nalysis and graph](analysis_and_graph.py)

## Data
The merged dataset is [data.csv](data.csv)
All the rest of the datasets are interim results created by [downloading_and_webscraping.py](downloading_and_webscraping.py).

## Graphs
All graphs are results created by [analysis_and_graph.py](analysis_and_graph.py)



### Project Description (Given by Jeff):
The goal of this project is to showcase your knowledge of Python by applying it to a 
research project of your own.  This is not a research methods course, so the quality of the
research is ancillary to the quality of your programming.

Your task is to find a minimum of two datasets available online, and then use Python to
download them using requests or Pandas, merge or concatenate them together, summarize the data 
with plots, tables and summary statistics, and then fit a simple model to it using Numpy, 
Scikit Learn, or Statsmodels.  The entire program must be organized using functions and/or 
classes, and it must run from start (downloading) to finish (making graphs, displaying tables, 
and model fitting) without stopping or requiring manual steps.  The use of other skills we have
or will learn in class, such as natural language processing, PDF scraping, and spatial data,
will be rewarded.

### Instructions
At least one part of your project should be challenging, and exhibit your coding skills.  For 
example, if you download two very easy datasets that are nicely structured and ready to work 
with, maybe you create some very elaborate plots.  If you instead download a very difficult
dataset that requires scraping unstructured data and complicated reshaping and merging, then
maybe you create some more straight-forward plots.  If both your plots and your data are
relatively simple, maybe you use natural language processing.  If you are in a group, you will
likely need more than one challenging section.

You will then spend **no more than 2-5 pages** writing your research findings up.  This is where 
you can discuss limitations as well.  For example, if you used an OLS model and got weak results, 
you might discuss what model you would have used in future research, or what additional data you
would want to find, or why the OLS wasn't a good choice.  Think of this writeup as a guide to 
your code, as much as it is an explanation of your research.  It should inform me of what I'm 
reading before I look at your code, so I am not trying to puzzle it out at the same time.

You may work on this project *alone* or in groups of *no more than three people*.  If you choose
to work alone, you will use your own repository like normal.  If you choose to use a group, you
must create your own team, [according to the instructions here](https://github.blog/2018-03-06-how-to-use-group-assignments-in-github-classroom/).

If there is a chance you will work in a group, do not create an individual repository and do not
commit any code.  Wait until you form a group, and then create a group repo.  *Once code has*
*been committed to a project, no group may be formed or added to.*

It is required that you use GitHub, and I will use your past commits to understand your thought
process for partial credit, and to monitor group participation.  You will not get full credit if
your repository does not show multiple commits as you build your project, especially for groups.
Expectations for the scope of the project will be higher for groups than for individuals, and the
division of labor will be up to each group.  Note again that I will be using your GitHub commit
history in grading, so while I will lean toward giving the same grade to everyone in a group, it 
is possible that group members will recieve different grades.

The link to create your project repository is available [here](https://classroom.github.com/g/V85WM5hs).

Any local path references must be defined in a logical way that allows me (or your groupmates)
to clone the repository and get to work with minimal changes (e.g. no more than one line of 
changes necessary).  That means hard coding your own computer path throughout your code will
result in lost points.

Remote retrieval of datasets should have a method of toggling the download attempt depending on
either a setting or by looking to see if the files are already downloaded.  This is best practice,
and will save me from having to download data for the entire class.

Your final repository must contain the following: 
1. Your code and commit history
2. The initial, *unmodified* dataframes you download
3. Saved .png versions of your plots
4. The final versions of the dataframe(s) you built
5. Your writeup (Word or markdown are both fine)

------

### Suggestions and Tips:
- Anywhere you can use things we learned in Data Skills 1 or 2, in a way that is relevant to 
your project, is a good idea.  For example, cleaning up your plots using some MatPlotLib 
methods we discussed is better than turning in vanilla MatPlotLib output, using formatting 
and other functions to clean up your data is better than displaying the same output in a 
messy fashion, and so on.
- You may use libraries and methods we did not go over in class, but ones that we did go over
should be preferred if they duplicate the functionality.  Remember all citation rules from 
the academic dishonesty policy in the syllabus.
- Effort put into organizing your code and making it readable, by, for example, following the
Python Style Guide and good usage of functions and variable names, will be rewarded.
- If you feel stuck coming up with research ideas, feel free to contact me or one of the TAs
so we can discuss your interests and make suggestions.
- Common merging and grouping parameters:
  - State
  - Country
  - Date
  - Names
- If your research idea is a much larger project, think of how you can develop a basic framework
for it using this project, which can then later be expanded into a proper research project.
- Remember that the point here is to showcase your Python coding, so do not get hung up for too
long on questions of research methodology.
- The entire point of reproducible research is to make it possible for others (and for a future
you who has had time to forget what you did and why) to understand, replicate, and modify your
work.  Keeping this in mind as you work will be good for your grade, and helpful to you in the
future if you expand on the project.