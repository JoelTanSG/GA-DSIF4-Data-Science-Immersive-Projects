
# ![](https://ga-dash.s3.amazonaws.com/production/assets/logo-9f88ae6c9c3871690e33280fcf557f33.png) Project 3: Web APIs & NLP
![](./assets/images/readme_banner.png)
[original image](https://preview.redd.it/ylzbphhjubh31.jpg?width=2400&format=pjpg&auto=webp&s=cfb70bd92d6ad2f0a954ae619ebf648b8d6461ac)

## Executive Summary
### Problem Statement
Project Scenario: A foreign company, is looking to establish its presence into Singapore and Malaysia. As part of a team of data analysts and data scientists in, I've been tasked by the marketing department to focus on the platform: Reddit, to explore what are the main concerns and topics of the day of the two countries. And using NLP to train model to identify if a user is from Singapore or Malaysia via the post made.
### Datasets used
The data used are scrapped from the subreddits: [r/singapore](https://www.reddit.com/r/singapore/) and [r/malaysia](https://www.reddit.com/r/malaysia/)
### Steps Taken
I first started the project by webscrapping 1,500 post from the subreddits: Malaysia and Singapore. From there I did some basic cleaning, removing digits and special characters from the titles. Upon realising that 80% of the post did not have any content, I decided to drop the text in the content.

Some interesting ideas were explored during the EDA.
1. Which netizens was more likely to embed media: Malaysia
2. What was the percentage of post tagged NSFW: less then 1% for both
3. Which subreddit was more active in terms of average comments: Singapore

I then generated word clouds to futher analyse the top subject or words from both community. Once I removed the current global topics of the war in Europe and the current virus pandemic, it could be clearly seen that the major concern of Singaporeans were: scam, time, and studies. While for the Malaysian, they were more concern with their education system and political figures/groups.

Finally using NLP I trained a few models that would be able to automatically detect if a post is coming from Singapore or Malaysia, but was not able to get a strong result. I strongly suspect that this is due to the data gather and cleaning stages and more could be done in that area. For now the model and analysis could perhaps give the team a rough indication on the users inclinations and location. But more work needs to be done.
### Recomendations and Future Steps
1. 1,500 post per subreddit is not enough. The top word count for each subreddit is less then 40. This could be a big reason why the random forest classifier fared so badly.
2. The datasets included post that were removed. This could explain why most post lack content. Perhaps a better way would be to filter and work with only posts that were still 'live'.
3. Following point 2, it would be more holistic if I could include or run the EDA and Modeling on the content itself rather then just the title.
4. As the Malaysia subreddit consisted of post in a mix of both English and Malay, I should have used an API like Google Translation API, to convert the text to english if possible. This would give better accuracy when using stopwords and lemma.
5. Mentioned earlier the content of the words used is very important in this project. There could be better results if a linguist who specialise in both countries spoken and written habits were to work together on this project.
6. The subreddits are not the full reflection of the countries' reddit population. As there are other splinter subreddits. For example, for singapore there is the [r/singaporeRaw](https://www.reddit.com/r/SingaporeRaw/),[r/singaporefi](https://www.reddit.com/r/singaporefi/), [r/asksingapore](https://www.reddit.com/r/askSingapore/), etc. To wider and more diverse set of data, these subreddits could be included for better analysis and model building.
### Limitations/ Disclaimer
- Malaysia's population as of 2020 is 32.37 million [source](https://datacommons.org/place/country/MYS?utm_medium=explore&mprop=count&popt=Person&hl=en) and Singapore's population in 2020 stood at 5.69 million [source](https://datacommons.org/place?utm_medium=explore&dcid=country/SGP&mprop=count&popt=Person&hl=en). The above analysis is only of 1,500 post made by different subredditors. Even if we were to assume each post is of a different person, that would make up less then 0.005% of the population in each country.

- Even though the subreddits are named Malaysia and Singapore, they're run on a global platform that is open for anyone to post or comment. As such some of these post could be from either countries or even citizens from other nations.
