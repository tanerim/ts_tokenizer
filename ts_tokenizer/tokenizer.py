import re
import sys
import multiprocessing
import json
import logging
from typing import List, Optional, Tuple, Union
from concurrent.futures import ProcessPoolExecutor
from ts_tokenizer.token_handler import TokenProcessor
from ts_tokenizer.char_fix import CharFix
from ts_tokenizer.output_format import OutputFormat, OutputFormatLike


def tokenize(
    line: str,
    return_format: OutputFormatLike = OutputFormat.TOKENIZED,
    output: bool = False,
) -> Union[str, List[Tuple[str, Optional[str]]]]:
    """
    Tokenize text using an OutputFormat member or a legacy string value.

    TOKENIZED returns one token per line; LINES returns space-separated tokens;
    TAGGED returns tab-separated token/tag pairs; TAGGED_LINES returns tuples.
    XML-only input returns a string. output=True enables JSON for structured
    formats. Invalid formats raise ValueError.
    """
    return_format = OutputFormat(return_format)
    processed_tokens = []
    # Strip whitespace and remove any invisible characters
    line = line.strip().replace('\u200b', '').replace('\ufeff', '')

    # Skip processing if the line is empty or contains only invisible characters
    if not line:
        logging.debug("Empty or whitespace-only line encountered. Skipping.")
        pass

    # Updated regex patterns to capture the tag name
    xml_open_tag = re.match(r'^<\s*/?\s*(\w+)(?:\s+\w+\s*=\s*(?:"[^"]*"|\'[^\']*\'))*\s*/?>$', line)
    xml_close_tag = re.match(r'^</\s*(\w+)\s*>$', line)

    xml_tag = None
    if xml_open_tag:
        xml_tag = (line.strip(), "XML_Tag")
        logging.debug(f"XML open tag detected: {xml_tag}")
    elif xml_close_tag:
        xml_tag = (line.strip(), "XML_Tag")
        logging.debug(f"XML close tag detected: {xml_tag}")

    if xml_tag:
        # Return the XML tag immediately in the specified format without further tokenization
        if return_format == 'tagged':
            result = json.dumps({"token": xml_tag[0], "tag": xml_tag[1]}, ensure_ascii=False) if output else "\t".join(
                xml_tag)
            logging.debug(f"Returning XML tag: {result}")
            return result
        else:
            logging.debug(f"Returning XML line unchanged: {line}")
            return line  # Return the original XML line unchanged if not in 'tagged' format
    else:
        # Proceed with tokenization only if the line is not an XML tag
        tokens = line.split()
        logging.debug(f"Tokens extracted: {tokens}")
        for token in tokens:
            try:
                processed_token = TokenProcessor.process_token(token)
                if isinstance(processed_token, tuple) and len(processed_token) >= 2:
                    processed_tokens.append(processed_token)
                elif isinstance(processed_token, list):
                    for subtoken in processed_token:
                        if isinstance(subtoken, tuple) and len(subtoken) >= 2:
                            processed_tokens.append(subtoken)
                        #else:
                        #    logging.error(f"Malformed subtoken detected: {subtoken}")
                #else:
                    #logging.error(f"Malformed token detected: {processed_token}")
            except Exception as e:
                logging.error(f"Error processing token '{token}': {e}", exc_info=True)

        # Handle output formats for non-XML tokens
        if return_format == 'tokenized':
            result = '\n'.join([token[0] for token in processed_tokens])

        elif return_format == 'tagged':
            if output:
                result = json.dumps(
                    [{"token": token[0], "tag": token[1]} for token in processed_tokens if len(token) >= 2],
                    ensure_ascii=False)
            else:
                # Only include tokens with the correct structure
                result = '\n'.join([f"{token[0]}\t{token[1]}" for token in processed_tokens if len(token) >= 2])

        elif return_format == 'lines':
            if output:
                result = json.dumps({"tokens": [token[0] for token in processed_tokens if len(token) >= 1]},
                                    ensure_ascii=False)
            else:
                result = ' '.join([token[0] for token in processed_tokens if len(token) >= 1])

        elif return_format == 'tagged_lines':
            if output:
                result = json.dumps(
                    [{"token": token[0], "tag": token[1] if len(token) > 1 else None} for token in processed_tokens],
                    ensure_ascii=False)
            else:
                result = [(token[0], token[1] if len(token) > 1 else None) for token in processed_tokens]

        logging.debug(f"Tokenization result: {result}")
        return result


class TSTokenizer:

    @staticmethod
    def ts_tokenize(input_file=None, filename=None, output_format: OutputFormatLike = OutputFormat.TOKENIZED, num_workers=None, verbose=False, output=False):
        """Print tokenized input; verbose is retained for compatibility only."""
        output_format = OutputFormat(output_format)
        if num_workers is None:
            num_workers = multiprocessing.cpu_count() - 1
            logging.debug(f"Number of workers set to {num_workers}")

        # Case 1: Handle piped input directly (input_text is provided)
        if input_file:
            logging.info("Processing input from stdin.")
            for line in input_file.splitlines():
                result = tokenize(line, output_format, output)
                if result is not None:
                    print(result)
            return

        # Case 2: Handle file input (filename is provided)
        if filename:
            logging.info(f"Processing file: {filename}")
            with open(filename, 'r', encoding='utf-8') as in_file:
                with ProcessPoolExecutor(max_workers=num_workers) as executor:
                    batch_size = 100
                    batch = []

                    # Process the file line by line
                    for line in in_file:
                        line = CharFix.fix(line)  # Apply CharFix without stripping spaces for XML tags

                        if line:  # Only process non-empty lines. Do not change
                            batch.append(line)
                        else:
                            pass

                        # When the batch size is reached, process the batch in parallel
                        if len(batch) >= batch_size:
                            logging.debug(f"Processing batch of size {len(batch)}")
                            futures = [executor.submit(tokenize, line, output_format, output) for line in batch]
                            for future in futures:
                                try:
                                    result = future.result()
                                    if result is not None:
                                        print(result)
                                except Exception as e:
                                    logging.error(f"Error processing line: {e}", exc_info=True)
                            batch = []  # Clear batch after processing

                    # Process remaining lines in the last batch
                    if batch:
                        logging.debug(f"Processing final batch of size {len(batch)}")
                        futures = [executor.submit(tokenize, line, output_format, output) for line in batch]
                        for future in futures:
                            try:
                                result = future.result()
                                if result is not None:
                                    print(result)
                            except Exception as e:
                                logging.error(f"Error processing line: {e}", exc_info=True)



if __name__ == "__main__":
    from ts_tokenizer.cli import main

    raise SystemExit(main())
