import argparse
import hashlib
import os
import time
from tqdm import tqdm

def ntlm_hash(input_string):
    return hashlib.new('md4', input_string.encode('utf-16le')).hexdigest()

def main(args):
    hash_file = args.output
    wordlist_file = args.wordlist
    progress_file = 'progress.txt'
    batch_size = args.batch_size

    # Initialize progress
    start_line = 0
    if os.path.exists(progress_file) and os.path.getsize(progress_file) > 0:
        with open(progress_file, 'r') as file:
            start_line = int(file.read().strip())

    with open(wordlist_file, 'r', encoding='utf-8', errors='ignore') as words:
        total_words = sum(1 for _ in words)

    with open(wordlist_file, 'r', encoding='utf-8', errors='ignore') as words, \
         open(hash_file, 'a') as hash_f, open(progress_file, 'w') as prog_f:
        hash_batch = []
        pbar = tqdm(total=total_words, unit="word", dynamic_ncols=True, mininterval=1.0)
        start_time = time.time()
        prev_time = start_time
        processed_words = 0  # Number of processed words
        for i, word in enumerate(words, start=1):
            if i < start_line:
                continue
            word = word.strip()  # Remove trailing newline
            hash_value = ntlm_hash(word)
            hash_batch.append(f'{word}: {hash_value}\n')

            if i % batch_size == 0:
                # Save hashes in batch
                hash_f.writelines(hash_batch)
                hash_batch = []

                # Save progress in batch
                prog_f.seek(0)
                prog_f.write(f'{i}\n')

                # Update progress bar
                pbar.update(batch_size)

                # Calculate elapsed time and remaining time
                curr_time = time.time()
                elapsed_time = curr_time - start_time
                time_per_word = elapsed_time / i
                remaining_words = total_words - i
                remaining_time = time_per_word * remaining_words

                # Update progress bar description
                pbar.set_description(f"Processing words ({i}/{total_words})")
                pbar.set_postfix({"Time Remaining": pbar.format_interval(remaining_time)})
                pbar.refresh()

            processed_words += 1

        # Save remaining hashes and progress if total_words is not a multiple of batch_size
        if hash_batch:
            hash_f.writelines(hash_batch)
            prog_f.seek(0)
            prog_f.write(f'{i}\n')

            # Update progress bar
            pbar.update(processed_words)

            # Calculate elapsed time and remaining time
            curr_time = time.time()
            elapsed_time = curr_time - start_time
            time_per_word = elapsed_time / i
            remaining_words = total_words - i
            remaining_time = time_per_word * remaining_words

            # Update progress bar description
            pbar.set_description(f"Processing words ({i}/{total_words})")
            pbar.set_postfix({"Time Remaining": pbar.format_interval(remaining_time)})
            pbar.refresh()

        pbar.close()

    # Print statistics
    elapsed = time.time() - start_time
    print("Job Statistics:")
    print(f"Total Words Processed: {total_words}")
    print(f"Total Time Elapsed: {elapsed:.2f} seconds")
    print(f"Average Time per Word: {elapsed/total_words:.6f} seconds")

def parse_args():
    parser = argparse.ArgumentParser(description="NTLM Rainbow Table Generator")
    parser.add_argument("-o", "--output", type=str, default="rainbow_hashes.txt", help="Output file for hashes (default: hashes.txt)")
    parser.add_argument("-w", "--wordlist", type=str, default="rockyou.txt", help="Wordlist file (default: rockyou.txt)")
    parser.add_argument("-b", "--batch-size", type=int, default=1000, help="Batch size for writing hashes (default: 1000)")
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    main(args)
