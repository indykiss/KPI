# Working notes, please ignore for now!

Sept 14 Notes:
Working on now/ in PMs
- Need to figure out yfinance ticker look up
    - Can implement for both client and custom index, basically same function

Work on this in AM/ early PM when brain is awake
- Need to figure out how to graph the two lines
    - Build the helper functions needed. 
        - Maybe just need 1 "calculate companies in arr growth" 
        - Before launch date, need all companies 
        - After launch date, all except client 
        - Problem is in how I'm calculcating growth now. I'm doing 
        for each company, calculate growth from start to end date.
        What I need to do is calculate growth from start to end, changing cos
- Build quick test suite
- After the above two things are done, CI/CD via Jenkins

Major steps:
1. Set up dash - Done

2. Input box with stock ticker - WIP
    - Need to look at Scottish dude's repo for how they organized
    the callbacks for this. I think maybe needs 2? 
    - Box exists, but isn't connected to yfinance

3. Input box with custom index of client competitors - WIP
    - Look in folder for list of companies in this industry 
    - Pull down GROWTH average. Will need to look at CapIQ for this bit. Includes industry PLUS this stock ticker
    - Selected industry, for test, will be in a CSV BUT will need to make this a actual database 

4. Input time - Done 

5. At this point, add deviation - Huge thing to work on. 
Build out a couple helper function options 
I'm thinking we build 2 lines that just overlap until launch date,
after launch date, there's a deviation. 
    - Stock price for client grows (ideally) in red
    - Industry growth continues in black line (but minus) client 
    - See output sketch for example output

6. Build simple test suite 
    Industry = Shoes: Nike, Timberland, Adidas, Asics
    Company: Timberland. 
    Pinpoint: Launch June 23, 2021  

    Expectations:
        - Industry loads
            - Industry list exists in folder 
            - All tickers on list exist 
        - Starting point is a time that exists (last 5 years max). Can't be in the future
        - Stock ticker exists 

7. Jenkins for CI/ CD
    - Super useful for quick deployment when adding in new industries
        - Probs could've done something with google sheets for self-service, 
        but is fine 
    - Can just add the industry.csv into indices folder and commit, done 


# Dash notes:
Two main components:
Layouts: Describes the tree of components that make up the application and how users experience content. Basically like React components but built in (dash_core_components, dash_html_components) 

Callbacks: Holds logic for dash app. Callbacks are automatically called whenever an input component's property changes. Can chain callbacks to trigger multiple updates in app. Callbacks are made of Inputs and Outputs. 


Notes / Extra features:
1. Add "request an industry" feature. Sends me an email
when people need to add a new subsection. Expect 1-2 weeks. 
Less relevant now (Sept 8) than when we first started, because I've set 
up the "custom index/ subindustry" droplist to actually pull stock price data.
Main issue is building a stock ticker LOOKUP instead of a hard coded thing. 

2. Use dcc.upload to allow users to input their own CSVs for sub-industries 
Again, less relevant. But saving point #2 in case we want to simplift due to 
time constraints later. 

