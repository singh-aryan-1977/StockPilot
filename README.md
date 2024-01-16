# StockPilot

This project is a web application built using Flask that serves as a technical screener for stock patterns. The application allows users to analyze stock patterns and find stocks in that current pattern, view generated tear sheets for that stock against their chosen benchmark, see whether it is in a bearish or bullish mode, and also view whether it is in squeeze (according to the TTM squeeze indicator) right now along with its candlestick chart showing the bollinger bonds and keltner channels. Please do not use this as the sole source for your investment advice.

## Running the program

To run the program, make sure you have these dependencies installed

    pip install flask pandas plotly matplotlib ta-lib quantstats yfinance

Before running the application, you need to ensure you have the necessary files downloaded. You can do this by first running the `snapshot.py` file via:

    python snapshot.py

or any other method you prefer. After that, ensure that you are in the `Screener` folder and run the following command:

    flask run

which will start a flask webapp on port 5000. Go to the url, `your_local_host:5000/snapshot`. After typing that command, the relevant files will be downloaded and you should get this message on completion:

![Picture showing success of snapshot](/Screener/images/image5.png)

From there,simply use the application on the default `your_local_host:5000/` page.

### Output

This is what you should get on start up:
![Image showing startup screen](/Screener/images/image.png)

Simply choose whichever pattern you want to analyze, and click the scan button. Here is the sample output for the pattern 'Advance Block'.
![Image showing when pattern selected](/Screener/images/image2.png)

From there, you can analyze the ticker's tearsheet by pressing the button, which will give you a screen as below:
![Image showing tearsheet for selected ticker](/Screener/images/image3.png)

You can scroll down for more information, and by default, it sets SPY as the benchmark but you can change it by typing yhe value of the ticker in the box above the tearsheet.

Lastly, the last column of the table shows whether the ticker is in squeeze or not, and by pressing it, you can see the candlestick chart of the ticker with the keltner channels and bollinger bonds.
![Image showing candlestick chart of selected ticker](/Screener/images/image4.png)
