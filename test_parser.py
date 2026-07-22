import re

def parse_podcast_script(script_text):
    """
    Parse a podcast script into [(speaker, text), ...].
    """
    segments = []
    warnings = []
    current_speaker = None

    speaker_pattern = re.compile(
        r'^\s*([\w][\w\s.\'-]{0,30}?)\s*[:\-–—]\s*(.*)$',
        re.UNICODE
    )

    for line_no, raw_line in enumerate(script_text.splitlines(), start=1):
        line = raw_line.strip()

        if not line:
            continue

        match = speaker_pattern.match(line)

        if match:
            speaker = match.group(1).strip()
            text = match.group(2).strip()

            if not text:
                current_speaker = speaker
                continue

            segments.append((speaker, text))
            current_speaker = speaker

        elif current_speaker:
            segments.append((current_speaker, line))

        else:
            warnings.append(
                f"Line {line_no}: could not identify a speaker in \"{line[:60]}\". "
                f"Expected a format like: CHARACTER: dialogue"
            )

    if not segments and not warnings:
        warnings.append("The script is empty. Add at least one line like: ARIA: Hello!")

    return segments, warnings


# ─── tests ───
tests = [
    "ARIA: Hello there",
    "ARIA : extra space before colon",
    "ARIA - dash instead of colon",
    "ARIA:\nline one\nline two",
    "just some text with no speaker",
    "",
    "ARIA: line one\nreal: line two\nARIA: line three",
]

for t in tests:
    segments, warnings = parse_podcast_script(t)
    print("INPUT:", repr(t))
    print("  segments:", segments)
    print("  warnings:", warnings)
    print()
tests = [
    "ARIA: Hello there",
    "ARIA : extra space before colon",
    "ARIA - dash instead of colon",
    "ARIA:\nline one\nline two",
    "just some text with no speaker",
    "",
    "ARIA: line one\nreal: line two\nARIA: line three",
]

for t in tests:
    segments, warnings = parse_podcast_script(t)
    print("INPUT:", repr(t))
    print("  segments:", segments)
    print("  warnings:", warnings)
    print()