# Working notes, please ignore for now!

Major steps:
1. Set up dash

2. Input box with stock ticker
    - Look at good stuff for this 
    - For v1 just make sure this loads 

3. Input box with selected industry 
    - Look in folder for list of companies in this industry 
    - Pull down GROWTH average. Will need to look at CapIQ for this bit. Includes industry PLUS this stock ticker
    - Selected industry, for test, will be in a CSV BUT will need to make this a actual database 

4. User inputs stock ticker, API call 
    - 

5. Input time. At this point, add deviation 
    - Stock price for client grows (ideally) in red
    - Industry growth continues in black line (but minus) client 

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
Ping directly if need more urgently. 
2. Use dcc.upload to allow users to input their own CSVs for sub-industries 
3. Use data table to double check the companies in the selected industry. Queries the database (do a database first)



