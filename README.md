# Dynamic Mutant Subsumption Graph Generator

## Summary
This application is designed to analyze the effectiveness of mutation testing by building a Dynamic Mutant Subsumption Graph (DMSG) from a set of test results. The DMSG helps researchers and developers:
- Understand redundancy among mutants.
- Identify a minimal set of essential mutants.
- Improve test suite efficiency by focusing on impactful mutants.
- Study the hierarchical relationships among mutants based on test behavior.

You can learn more about the concept by reading [this paper](https://homes.cs.washington.edu/~rjust/publ/prioritizing_mutants_tcap_icse_2022.pdf).

## Prerequisites
- Python 3
- pip package manager

## Required Python Packages
Run `pip install -r requirements.txt`

You can also install them manually:
- Flask
- matplotlib
- networkx

Note: I recommend running this on an Anaconda environment or Python notebook for simplicity of installation. If you are having trouble, try running pip using administrator command line.

## Running the Application
1. Download and unzip the program source code.
2. Run the Flask app: `python app.py`
3. By default, the app runs at [127.0.0.1:5000](http://127.0.0.1:5000)

## Using the Web Interface
1. Open the app URL in your browser.
2. Upload your kill map CSV file. (If you need a sample kill map CSV file, you can find it in the `/uploads` folder of the source code directory. You can simply upload that file for testing.)
3. Wait a moment while the graph is generated.
4. The image will generate soon afterwards. Below the image, a list of dominator mutants is displayed.

## CSV Input Format
The uploaded CSV must have 3 columns:
`TestNo,MutantNo,Status`

TestNo is an integer
MutantNo is an integer
Status is a string that is either "FAIL", "TIME", or "EXC"

Each row indicates whether a test kills a mutant.

You can also generate kill maps for a sample Triangle program using [this mutant analysis program](https://bitbucket.org/rjust/mutation).

## How It Works — Technical Details
- Equivalent mutants (those killed by exactly the same tests) are merged into one node labeled with their mutant numbers, separated by commas.
- The DMSG is a directed acyclic graph where edges represent subsumption relations.
- The graph is topologically layered: Nodes on the same level share the same horizontal row.
- Dominators are nodes w/ zero incoming edges aka mutants not subsumed by any other

## Troubleshooting
### "No file part" or "No selected file" error? 
Make sure to select a CSV file before submitting.

### Malformed CSV errors? 
Check that your CSV columns are named exactly TestNo, MutantNo, Status and that Status contains FAIL, TIME, or EXC.

### Graph image not showing? 
Confirm the `static/` folder exists and Flask has write permissions there.
