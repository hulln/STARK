# Report: Criteria for Splitting the GUM Corpus

The **GUM corpus** was divided into **spoken** and **written** documents according to specific classification criteria:

### Classification Criteria:

1. **Genre-based classification**:
   - Documents with genres from a predefined set of spoken genres: *court*, *interview*, *conversation*, *dialogue*, *speech*, *podcast*, *vlog* were classified as spoken.

2. **Speaker count**:
   - Documents with at least one speaker (`speakerCount > 0`) were classified as spoken, except for the genres *fiction* and *letter*, which were manually checked and classified as written, despite meeting the spoken criteria.

3. **Written classification**:
   - All other documents that did not meet the spoken genre criteria and had **zero speakers** (`speakerCount = 0`) were classified as written.

---

### Statistics Summary:

#### Speaker Counts and Occurrences (whole corpus):

| **Speaker Count** | **Occurrences** |
|-------------------|-----------------|
| 0                 | 127 documents   |
| 1                 | 25 documents    |
| 2                 | 28 documents    |
| 3                 | 16 documents    |
| 4                 | 12 documents    |
| 5                 | 4 documents     |
| 6                 | 4 documents     |
| 8                 | 1 document      |

---

#### Genre and Document Counts:

| **Documents (Spoken)** | **Documents (Written)** |
|------------------------|-------------------------|
| conversation (14)      | academic (18)           |
| court (6)              | bio (20)                |
| interview (19)         | essay (5)               |
| podcast (5)            | fiction (19)            |
| speech (15)            | letter (6)              |
| vlog (15)              | news (23)               |
|                        | textbook (15)           |
|                        | voyage (18)             |
|                        | whow (19)               |

---

#### File Statistics:

| **File**            | **Documents** | **Paragraphs** | **Sentences** |
|-------------------------|---------------|----------------|---------------|
| Spoken                  | 74            | 4766           | 5653          |
| Written                 | 143           | 5114           | 6493          |
| Total                   | 217           | 9880           | 12146         |

---

#### Token Statistics:

| **Type**         | **Single Number Tokens** | **Range Tokens** | **Total Tokens** |
|------------------|--------------------------|------------------|------------------|
| Spoken           | 80,930                   | 2,382            | 83,312           |
| Written          | 130,990                  | 1,207            | 132,197          |
| Total            | 211,920                  | 3,589            | 215,509          |

- **Single Number Tokens**: Counted when a row starts with a digit followed by a space and does not contain a hyphen (e.g. "1", "2", "24").
- **Range Tokens**: Cases like number ranges (e.g. "1-2", "5-6").