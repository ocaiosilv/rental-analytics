##  Study Project: Data Pipeline

###  Objective

This is a simple project used to explore how a data pipeline works, providing an introduction to:
* **Data Collection and Cleaning** (Web Scraping)
* **Analysis and Visualization** (EDA)
* **Application of a (simple) prediction model**

Although the prediction model yielded limited results, the project was crucial for exploring the workflow and learning essential libraries like **Pandas, Matplotlib, and Scikit-learn**.

###  How to Run

1.  **Install Dependencies:**
    ```bash
    pip install pandas matplotlib seaborn scikit-learn cloudscraper beautifulsoup4
    ```
2.  **Execute Data Collection:**
    ```bash
    python scrapping.py
    ```
3.  **Explore the Analysis:**
    Open and run the notebooks (`DataAnalysis.ipynb` and `machinelearn.ipnyb`).

###  Files

* `scrapping.py`: Data collector.
* `DataAnalysis.ipynb`: Exploratory Data Analysis and Visualization.
* `machinelearn.ipnyb`: Application of the Linear Regression model.

###  General Considerations

Overall, the project proved very useful for exploring the concept of a pipeline and for practicing code maintenance/refactoring on GitHub. Although its performance was not exactly relevant due to the nature of the collected data (rental prices did not follow a fixed pattern, but rather the individual evaluation of the owner) and the lack of more relevant data for this survey, such as proximity to points of interest.
