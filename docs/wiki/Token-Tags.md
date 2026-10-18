# Token tags

The following table is the existing rule and tag reference. Rows marked `No`
represent processing rules without a standalone output tag.

| #  | Function                    | Sample                       | Used As Output | Tag                |
|----|-----------------------------|------------------------------|----------------|--------------------|
| 01 | is_mention                  | @ts-tokenizer                | Yes            | Mention            |
| 02 | is_hashtag                  | #ts-tokenizer                | Yes            | Hashtag            |
| 03 | is_mention_suffix           | @defne'den                   | Yes            | Mention_Suffix     |
| 04 | is_hashtag_suffix           | #haber'ler                   | Yes            | Hashtag_Suffix     |
| 05 | is_in_quotes                | "ts-tokenizer"               | No             | -----              |
| 06 | is_numbered_title           | (1)                          | Yes            | Numbered_Title     |
| 07 | is_in_paranthesis           | (bilgisayar)                 | No             | -----              |
| 08 | is_date_range               | 01.01.2024-01.01.2025        | Yes            | Date_Range         |
| 09 | is_complex_punc             | -yeniden,sonradan..          | No             | -----              |
| 10 | is_date                     | 22.02.2016                   | Yes            | Date               |
| 11 | is_hour                     | 14.05                        | Yes            | Hour               |
| 12 | is_percentage_numbers       | %75                          | Yes            | Percentage_Numbers |
| 13 | is_percentage_numbers_chars | %75'lik                      | Yes            | Percentage_Numbers |
| 14 | is_roman_number             | XI                           | Yes            | Roman_Number       |
| 15 | is_bullet_list              | •Giriş                       | Yes            | Bullet_List        |
| 16 | is_email                    | tanersezerr@gmail.com        | Yes            | Email              |
| 17 | is_email_punc               | tanersezerr@gmail.com.       | No             | -----              |
| 18 | is_full_url                 | https://tscorpus.com         | Yes            | Full_URL           |
| 19 | is_web_url                  | www.tscorpus.com             | Yes            | Web_URL            |
| 20 | is_full_url                 | www.tscorpus.com'un           | Yes            | URL_Suffix         |
| 21 | is_copyright                | ©tscorpus                    | Yes            | Copyright          |
| 22 | is_registered               | tscorpus®                    | Yes            | Registered         |
| 23 | is_trademark                | tscorpus™                    | Yes            | Trademark          |
| 24 | is_currency                 | 100$                         | Yes            | Currency           |
| 25 | is_num_char_sequence        | 380A                         | No             | -----              |
| 26 | is_abbr                     | TBMM                         | Yes            | Abbr               |
| 27 | is_in_lexicon               | bilgisayar                   | Yes            | Valid_Word         |
| 28 | is_in_exceptions            | e-mail                       | Yes            | Exception          |
| 29 | is_in_eng_words             | computer                     | Yes            | English_Word       |
| 30 | is_smiley                   | :)                           | Yes            | Smiley             |
| 31 | is_multiple_smiley          | :):)                         | No             | -----              |
| 32 | is_emoticon                 | 🍻                           | Yes            | Emoticon           |
| 33 | is_multiple_emoticon        | 🍻🍻                         | No             | -----              |
| 34 | is_multiple_smiley_in       | hey:):)                      | No             | -----              |
| 35 | is_number                   | 175.01                       | Yes            | Number             |
| 36 | is_apostrophed              | Türkiye'nin                  | Yes            | Apostrophed        |
| 37 | is_single_punc              | !                            | Yes            | Punc               |
| 38 | is_multi_punc               | !!                           | No             | -----              |
| 39 | is_single_hyphenated        | sabah-akşam                  | Yes            | Single_Hyphenated  |
| 40 | is_multi_hyphenated         | çay-su-kahve                 | Yes            | Multi-Hyphenated   |
| 41 | is_single_underscored       | Gel_Git                      | Yes            | Single_Underscored |
| 42 | is_multi_underscored        | Yarı_Yapılandırılmış_Mülakat | Yes            | Multi_Underscored  |
| 43 | is_one_char_fixable         | bilgisa¬yar                  | Yes            | One_Char_Fixed     |
| 44 | is_formula                  | F(2,37)=6.42                 | Yes            | Formula            |
| 45 | is_three_or_more            | heyyyyy                      | No             | -----              |
| 46 | is_fsp                      | bilgisayar.                  | No             | -----              |
| 47 | is_isp                      | .bilgisayar                  | No             | -----              |
| 48 | is_fmp                      | bilgisayar..                 | No             | -----              |
| 49 | is_imp                      | ..bilgisayar                 | No             | -----              |
| 50 | is_msp                      | --bilgisayar--               | No             | -----              |
| 51 | is_mssp                     | -bilgisayar-                 | No             | -----              |
| 52 | is_midsp                    | okul,öğrenci                 | No             | -----              |
| 53 | is_midmp                    | okul,öğrenci, öğretmen       | No             | -----              |
| 54 | is_non_latin                | 한국드                          | No             | Non_Latin          |
