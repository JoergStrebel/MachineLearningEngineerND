# Machine Learning Engineer Nanodegree
## Capstone Proposal
Jörg Strebel  
October 10th 2019

## Proposal
_(approx. 2-3 pages)_

### Domain Background
_(approx. 1-2 paragraphs)_
```In this section, provide brief details on the background information of the domain from which the project is proposed. 
Historical information relevant to the project should be included.
``` 
As people age, they inevitably retire from their jobs to live off their savings. If you google for "retirement investing today", 
you will find around 143 million related web pages on the WWW. So the topic is very relevant to many people. In Germany, 
a regular employee has to 
spend a certain percentage of his salary on a state-run insurance, but they can also opt to save more an put the money 
into financial products to secure their financial needs during retirement. One possible way to invest money for retirement 
is to participate in the stock market. This option has become more important over the last 10 years, as the fixed-interest 
investment opportunities have largely vanished or yield unsatisfactory profits.

```
Motivation - It should be clear how or why a problem in the domain can or should be solved.
``` 
If a person then chooses to use the stock market for long-term retirement investment, they need to have a sound and secure 
investment strategy, i.e. how much to invest, when to buy, what to buy (or sell). Ideally, the strategy leads to a long and steady 
increase of the value of the portfolio, so that the money is available when they retire. 
Now the problem arises , how the individual can come up with such a strategy. 

```
Related academic research should be appropriately cited in this section, including why that research is relevant.
``` 
https://www.sciencedirect.com/science/article/abs/pii/S0304405X06001127
https://www.tandfonline.com/doi/abs/10.1080/10920277.2000.10595899

INVESTING FOR RETIREMENT: USING THE PAST TO MODEL THE FUTURE.
https://web.b.ebscohost.com/abstract?direct=true&profile=ehost&scope=site&authtype=crawler&jrnl=10403981&AN=5558183&h=eT7kaJlvwTYF03fBKPVPAjxrYbbIg71Il8Becp1HEiwL8qqWbRJWMYAXYjBqROYHIY%2fvI3OxVdeCqEclAZfgpQ%3d%3d&crl=c&resultNs=AdminWebAuth&resultLocal=ErrCrlNotAuth&crlhashurl=login.aspx%3fdirect%3dtrue%26profile%3dehost%26scope%3dsite%26authtype%3dcrawler%26jrnl%3d10403981%26AN%3d5558183

https://patents.google.com/patent/US7398241B2/en



I also have a personal motivation to investigate this problem, as I am an active investor at German, European and US 
stock exchanges (mainly ETFs). If this project is successful, it will be very helpful for my investment decisions.  


### Problem Statement
_(approx. 1 paragraph)_

long-term investment strategy under budget and time constraints on European ETFs suitable for retirement investing.

```
In this section, clearly describe the problem that is to be solved. The problem described should be well defined and 
should have at least one relevant potential solution. Additionally, describe the problem thoroughly such that it is 
clear that the problem is quantifiable (the problem can be expressed in mathematical or logical terms) , 
measurable (the problem can be measured by some metric and clearly observed), and replicable 
(the problem can be reproduced and occurs more than once).
```

### Datasets and Inputs
_(approx. 2-3 paragraphs)_

```
In this section, the dataset(s) and/or input(s) being considered for the project should be thoroughly described, such 
as how they relate to the problem and why they should be used. Information such as how the dataset or input is (was) 
obtained, and the characteristics of the dataset or input, should be included with relevant references and citations 
as necessary It should be clear how the dataset(s) or input(s) will be used in the project and whether their use is 
appropriate given the context of the problem.
```



### Solution Statement
_(approx. 1 paragraph)_

```
In this section, clearly describe a solution to the problem. The solution should be applicable to the project domain and 
appropriate for the dataset(s) or input(s) given. Additionally, describe the solution thoroughly such that it is clear 
that the solution is quantifiable (the solution can be expressed in mathematical or logical terms) , measurable 
(the solution can be measured by some metric and clearly observed), and replicable (the solution can be reproduced and 
occurs more than once).
```

I would like to suggest a reinforcement-learning based agent as a solution. The agent would decide when to trade and 
how much to buy from the three given ETFs. It is also supposed to stay within the given budget constraints. The agent 
learns a trading strategy based on historical stock data and then runs daily and outputs the percentage amounts to buy 
or sell from the funds in the portofolio.
The goal is not to generate sustainable or supreme  
&alpha; ([Definition](https://www.investopedia.com/articles/investing/092115/alpha-and-beta-beginners.asp)), but to 
automate the investment decision (and free the investor of manual labour).  

[Wikifolio](https://www.wikifolio.com/de/de/home), a German company, uses a social media platform to share investment 
portfolios of platform members and offers the chance to investors to put their money in one of these portfolios. If a 
trading agent was successful, it could be used there as well.      


### Benchmark Model
_(approximately 1-2 paragraphs)_

```
In this section, provide the details for a benchmark model or result that relates to the domain, problem statement, and 
intended solution. Ideally, the benchmark model or result contextualizes existing methods or known information in the 
domain and problem given, which could then be objectively compared to the solution. Describe how the benchmark model or 
result is measurable (can be measured by some metric and clearly observed) with thorough detail.
```

The benchmark for my proposed RL trading algorithm would be a passive dollar-cost averaging strategy 
([Link](https://en.wikipedia.org/wiki/Dollar_cost_averaging)) in combination with a buy-and-hold strategy 
([Link](https://en.wikipedia.org/wiki/Buy_and_hold)). In essence, the investor regularly buys investment products for a 
constant amount of money and then holds these products for a long period of time. Such a strategy would typically be 
found with long-term investors building a retirement portfolio.   

This strategy minimizes risk, but it may also overlook opportunities and does not take advantage of the market direction.
The benchmark strategy is implemented in the same programming framework as the RL agent and it is compared on the same 
data from the same financial products.
 

### Evaluation Metrics
_(approx. 1-2 paragraphs)_

```
In this section, propose at least one evaluation metric that can be used to quantify the performance of both the 
benchmark model and the solution model. The evaluation metric(s) you propose should be appropriate given the context of 
the data, the problem statement, and the intended solution. Describe how the evaluation metric(s) are derived and 
provide an example of their mathematical representations (if applicable). Complex evaluation metrics should be clearly 
defined and quantifiable (can be expressed in mathematical or logical terms).
```
The actual metric to compare both strategies will be percentage returns per time period.

### Project Design
_(approx. 1 page)_

```
In this final section, summarize a theoretical workflow for approaching a solution given the problem. Provide thorough 
discussion for what strategies you may consider employing, what analysis of the data might be required before being 
used, or which algorithms will be considered for your implementation. The workflow and discussion that you provide 
should align with the qualities of the previous sections. Additionally, you are encouraged to include small 
visualizations, pseudocode, or diagrams to aid in describing the project design, but it is not required. 
The discussion should clearly outline your intended workflow of the capstone project.
```

### References

-----------

**Before submitting your proposal, ask yourself. . .**

- Does the proposal you have written follow a well-organized structure similar to that of the project template?
- Is each section (particularly **Solution Statement** and **Project Design**) written in a clear, concise and specific fashion? Are there any ambiguous terms or phrases that need clarification?
- Would the intended audience of your project be able to understand your proposal?
- Have you properly proofread your proposal to assure there are minimal grammatical and spelling mistakes?
- Are all the resources used for this project correctly cited and referenced?
