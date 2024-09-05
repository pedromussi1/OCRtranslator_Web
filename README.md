
<h1 align="center">Comic Recognizer</h1>

<p align="center">
  <a href="https://www.youtube.com/watch?v=h8sp7vFeV7c"><img src="https://i.imgur.com/uPkoNw1.gif" alt="YouTube Demonstration" width="800"></a>
</p>

<p align="center">A machine learning-powered web application to identify comic books by their covers, built with Flask and TensorFlow.</p>

<h2>Description</h2>

<p>The goal of this project was to develop a program that uses image recognition to identify comic books based on their covers. Built with Flask and a custom-trained machine learning model, the application allows users to upload an image of a comic book cover and receive identification results. The system processes and classifies the uploaded images, providing users with relevant information about the comic book. This tool can be particularly useful for comic book collectors, retailers, and enthusiasts.</p>

<h2>Languages and Utilities Used</h2>
<ul>
    <li><b>Flask:</b> Serves the web application and handles routing.</li>
    <li><b>Python:</b> Core programming language for logic and model integration.</li>
    <li><b>TensorFlow:</b> Used to build and train the image classification model.</li>
    <li><b>OpenCV:</b> Handles image processing tasks before classification.</li>
    <li><b>HTML/CSS/JavaScript:</b> Builds the frontend interface.</li>
    <li><b>NumPy:</b> Performs numerical operations on image data.</li>
    <li><b>Pandas:</b> Used for data manipulation and preparation.</li>
</ul>


<h2>Environments Used</h2>

<ul>
  <li><b>Windows 11</b></li>
  <li><b>Visual Studio Code</b></li>
</ul>

<h2>Installation</h2>
<ol>
    <li><strong>Clone the Repository:</strong>
        <pre><code>git clone https://github.com/yourusername/comic-book-identifier.git
cd comic-book-identifier</code></pre>
    </li>
    <li><strong>Create and Activate a Virtual Environment:</strong>
        <pre><code>python -m venv .venv
source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`</code></pre>
    </li>
    <li><strong>Install Dependencies:</strong>
        <pre><code>pip install -r requirements.txt</code></pre>
    </li>
    <li><strong>Add Your Model and Data:</strong>
        <ul>
            <li>Place your trained model file (e.g., <code>model.h5</code>) in the <code>static/models</code> directory.</li>
            <li>Ensure your dataset is properly organized in the <code>data</code> directory.</li>
        </ul>
    </li>
    <li><strong>Run the Application:</strong>
        <pre><code>python app.py</code></pre>
        The application will start and be accessible at <code>http://127.0.0.1:5000/</code>.
    </li>
</ol>

<h2>Usage</h2>
<ol>
    <li>Open the application in your web browser.</li>
    <li>Choose a comic book cover image from your local files using the file input field.</li>
    <li>Click the "Identify Comic" button to upload the image and process it.</li>
    <li>The result will display below the upload form, showing the identified comic book.</li>
</ol>

<h2>Code Structure</h2>
<ul>
    <li><strong>app.py:</strong> Main application file, contains routes and logic for preprocessing and classification.</li>
    <li><strong>static/:</strong> Contains static files such as CSS, JavaScript, and images.</li>
    <li><strong>templates/:</strong> HTML templates for rendering the web pages.</li>
    <li><strong>data/:</strong> Contains image data and any additional resources.</li>
    <li><strong>models/:</strong> Stores the trained machine learning model.</li>
</ul>

<h2>Known Issues</h2>
<ul>
    <li>Images with different backgrounds may affect the identification accuracy.</li>
    <li>The application may require fine-tuning for better performance on diverse datasets.</li>
</ul>


<h2>Contributing</h2>
<p>Contributions are welcome! Please fork the repository, create a new branch, and submit a pull request with your changes. For major changes, please open an issue first to discuss what you would like to change.</p>

<p>

<h2>
<a href="https://github.com/pedromussi1/comic-recognizer/blob/main/READCODE.md">Code Breakdown Here!</a>
</h2>

<h3>Comic Book Cover</h3>

<p align="center">
  <kbd><img src="https://i.imgur.com/SrQ3qVB.png" alt="ComicBook" width="900"></kbd>
</p>

<p>The main page gives the option for the user to choose a comic cover from their computer. Clicking on "identify Comic" before choosing a comic cover will do nothing.</p>

<hr>

<h3>Choosing a file</h3>

<p align="center">
  <kbd><img src="https://i.imgur.com/HvubM7R.png" alt="ChoosingCover"></kbd>
</p>

<p>After clicking on "Choose a Comic Cover", you will click on the image with a comic book cover you want to identify and click "Open".</p>

<hr>

<h3>Analyzing the file</h3>

<p align="center">
  <kbd><img src="https://i.imgur.com/tZLRLJb.png" alt="TranslatingText"></kbd>
</p>

<p>After choosing your file, you will see a thumbnail for the image you selected, and you can proceed by clicking on "identify Comic".</p>

<hr>

<h3>Results</h3>

<p align="center">
  <kbd><img src="https://i.imgur.com/ZWw2c59.png" alt="TranslatingText"></kbd>
</p>

<p>You will then see what the program identified your comic book to be. You can also click on "Go Back" and try the progrma again with a different comic book cover.</p>

