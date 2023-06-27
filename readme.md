# NTLM Rainbow Table Generator

The NTLM Rainbow Table Generator is a command-line tool for generating NTLM hashes from a wordlist. It utilizes the MD4 algorithm to calculate the hash value for each word in the wordlist and saves the results to an output file.

**Please note, this project is WIP the progress.txt contains a running count for restart fallback, please reset to 0 manually**

## Usage

```commandline
python rainbow_gen.py [-h] [-o OUTPUT] [-w WORDLIST] [-b BATCH_SIZE]
```


### Arguments

- `-h, --help`: Show the help message and exit.
- `-o OUTPUT, --output OUTPUT`: Specify the output file for saving the generated hashes. (default: hashes.txt)
- `-w WORDLIST, --wordlist WORDLIST`: Specify the wordlist file containing the words to generate hashes. (default: rockyou.txt)
- `-b BATCH_SIZE, --batch-size BATCH_SIZE`: Specify the batch size for writing hashes to the output file. (default: 1000)

## Example

```
python3 rainbow_gen.py -o myhashes.txt -w mywordlist.txt
```

This will generate hashes using the `mywordlist.txt` file and save the results in the `myhashes.txt` file.

## Job Statistics

After the execution of the script is completed, it will display statistics about the generated hashes. The following statistics will be printed:

- Total Words Processed: The number of words processed from the wordlist.
- Total Time Elapsed: The total time taken to generate the hashes.
- Average Time per Word: The average time taken to generate a hash for each word.

These statistics provide insights into the performance and progress of the NTLM Rainbow Table generation process.

---

