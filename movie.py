import os
import re
from moviepy import TextClip, concatenate_videoclips

SCRIPT_PATH = os.path.join('funeral_ops', 'broadcast_brief_script.md')
OUTPUT_VIDEO = 'ZAFSA_CIRCULAR_BRDCST_LN53.mp4'


def parse_script(path: str):
    """Parse key lines from the broadcast script."""
    lines = []
    with open(path, 'r') as f:
        for line in f:
            line = line.strip()
            if re.match(r'^\d+\.', line):
                # Remove leading digits and period
                lines.append(re.sub(r'^\d+\.\s*', '', line))
            elif line.startswith('"') and line.endswith('"'):
                lines.append(line.strip('"'))
    return lines


def create_video(lines, output_path: str, duration: int = 5):
    """Create a simple slideshow video from text lines."""
    clips = []
    for text in lines:
        clip = (
            TextClip(
                text=text,
                font="DejaVuSans-Bold",
                font_size=48,
                color='white',
                bg_color='black',
                method='caption',
                size=(1920, 1080),
                text_align='center',
            )
            .with_duration(duration)
        )
        clips.append(clip)
    final = concatenate_videoclips(clips, method='compose')
    final.write_videofile(output_path, fps=24)


def main():
    lines = parse_script(SCRIPT_PATH)
    if not lines:
        raise ValueError('No lines found in script.')
    create_video(lines, OUTPUT_VIDEO)


if __name__ == '__main__':
    main()
