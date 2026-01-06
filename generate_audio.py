#!/usr/bin/env python3
"""
Generate TTS audio using espeak-ng for offline TTS
and create precise timestamp file for visual synchronization.

Note: This uses espeak-ng as Kokoro TTS requires internet access to HuggingFace.
The timestamps are designed for future use with higher quality TTS like Kokoro af_bella.
"""

import json
import wave
import subprocess
import os
import re

# Script sections with narration text (extracted from binary_search_script.md)
SCRIPT_SECTIONS = [
    {
        "section": "INTRODUCTION",
        "text": """Imagine you're looking for a word in a dictionary. Not just any dictionary—one with fifty thousand words. You could start at the very first page and flip through one by one until you find it. But that would take forever, wouldn't it?

Here's the thing: nobody actually does that. Instead, you open the dictionary somewhere in the middle, see where you are, and then decide whether to go forward or backward. And without even thinking about it, you've just used one of the most elegant and powerful ideas in all of computer science.

This is binary search.

At first glance, it might seem almost too simple to be interesting. You're just cutting things in half, over and over again. But there's something remarkable hiding beneath that simplicity—something that reveals a deep truth about how we can dramatically speed up the process of finding things.

Today, I want to show you not just what binary search does, but why it works so beautifully, and why that matters far more than you might expect."""
    },
    {
        "section": "THE_PROBLEM_LINEAR_SEARCH",
        "text": """Let's start with a concrete problem. Say you have a sorted list of one million numbers, and you want to find a specific value—let's call it target.

The most straightforward approach? Start at the beginning and check each element one by one. This is called linear search, and it works perfectly fine. But here's the catch: in the worst case, you might need to check all one million numbers before finding what you're looking for. Or worse—you check everything only to discover the number isn't there at all.

Now, one million comparisons might sound manageable for a computer. But what if you had a billion entries? Ten billion? And what if you needed to perform this search thousands of times per second?

This is where things get interesting. Because binary search doesn't just make this faster—it makes it dramatically faster. So much faster that it almost feels like cheating.

With binary search on one million sorted elements, you'll find your answer in at most... twenty comparisons. Let that sink in. Not one million. Not one thousand. Twenty.

How is that even possible?"""
    },
    {
        "section": "THE_CORE_INSIGHT_POWER_OF_HALVING",
        "text": """The secret lies in a simple but profound observation: when you make a single comparison in a sorted list, you don't just eliminate one possibility—you eliminate half of all remaining possibilities.

Here's how it works. You look at the middle element. If it's exactly what you're looking for, great—you're done. But even if it's not, you've learned something incredibly valuable. If your target is smaller than the middle element, you know—with absolute certainty—that it cannot be in the upper half of the list. So you throw away that entire half and focus only on what remains.

And here's the beautiful part: you do the exact same thing again. Look at the middle of the remaining section. Compare. Eliminate half. Repeat.

Each step doesn't add or subtract a constant amount from your problem. Each step divides your problem in half. And division is extraordinarily powerful.

Think about it this way. If you have one million elements:
After one comparison, you have at most five hundred thousand left.
After two comparisons, two hundred fifty thousand.
After ten comparisons, fewer than a thousand.
After twenty comparisons, you're down to one.

This is logarithmic behavior. And it's why binary search can handle massive datasets with almost effortless efficiency."""
    },
    {
        "section": "THE_ALGORITHM_IN_ACTION",
        "text": """Let me walk you through exactly how this plays out.

We maintain two boundaries—let's call them left and right. Initially, left points to the first element and right points to the last. These boundaries define the portion of the list where our target could still possibly exist.

At each step, we calculate the middle position—roughly halfway between left and right. We then compare the element at this middle position to our target.

If they match, we've found it. Search complete.

If the target is smaller, we know it must be in the left portion. So we move the right boundary to just before the middle, effectively discarding the entire right half.

If the target is larger, we do the opposite. We move the left boundary to just after the middle, discarding the left half.

We keep repeating this process. The search space shrinks by half with each iteration—left and right drawing ever closer together. Eventually, either we find the target, or the boundaries cross each other, telling us the target doesn't exist in the list.

There's an elegance to this dance of pointers. Each movement is purposeful. Each comparison carries maximum information. Nothing is wasted."""
    },
    {
        "section": "THE_MATHEMATICS_LOGARITHMS",
        "text": """Let's put some precise numbers to this intuition.

If we start with n elements, after one step we have at most n divided by two. After two steps, n divided by four. After k steps, n divided by two to the power of k.

We want to know: how many steps until we're down to just one element?

That's when n divided by two to the k equals one. Solving for k gives us k equals log base two of n.

For one million elements, log base two of one million is approximately twenty. For one billion, it's about thirty. For a trillion, just forty.

This is the magic of logarithmic time. The number of steps grows incredibly slowly compared to the size of the input. Double your data? Add just one more comparison. Multiply your data by a thousand? Add only ten more comparisons.

Linear search says: "Your problem is twice as big, so I need twice as much time."

Binary search says: "Your problem is twice as big, so I need... one more step."

That difference is the difference between algorithms that scale and algorithms that don't."""
    },
    {
        "section": "COMMON_PITFALLS",
        "text": """Now, despite its conceptual simplicity, binary search is famously tricky to implement correctly. Let me highlight a few subtleties that have tripped up countless programmers.

First, calculating the middle index. The naive approach—adding left and right, then dividing by two—can actually overflow for large values. A safer technique is to compute left plus the difference between right and left, divided by two.

Second, the boundary updates. Should you set right to mid, or to mid minus one? Should left become mid, or mid plus one? Getting this wrong can lead to infinite loops where the pointers never converge, or off-by-one errors where you accidentally skip the target.

Third, the loop condition. Is it "while left is less than right" or "while left is less than or equal to right"? The choice depends on how you handle the boundaries.

These details might seem pedantic, but they matter enormously. In fact, studies have shown that most programmers, even experienced ones, get binary search wrong on their first attempt. The lesson? Test carefully, think through edge cases, and trace through your logic step by step."""
    },
    {
        "section": "BEYOND_SEARCHING",
        "text": """But here's what I find most fascinating about binary search. Its power extends far beyond just finding elements in a sorted list.

The underlying principle—eliminating half of the possibilities with each step—appears throughout computer science and mathematics. It's the same idea behind bisection methods for finding roots of equations. It's how git bisect helps you find the exact commit that introduced a bug. It's used in optimization algorithms, in compression, in machine learning.

Whenever you can frame a problem as a series of yes-or-no questions where each answer eliminates half the remaining options, you're tapping into this same logarithmic magic.

Binary search isn't just an algorithm. It's a way of thinking—a reminder that the structure of information, when properly exploited, can transform the seemingly impossible into the trivially easy."""
    },
    {
        "section": "CLOSING",
        "text": """So the next time you flip open a dictionary or scroll through a sorted list, remember: you're not just searching. You're wielding one of the most powerful ideas in computation—an idea that turns millions into twenty, that transforms linear slogs into logarithmic leaps.

And that, in the end, is why binary search matters. Not because it's fast—though it certainly is. But because it shows us what becomes possible when we think carefully about the structure of our problems."""
    }
]


def split_into_sentences(text):
    """Split text into sentences for timestamp tracking."""
    # Split on sentence-ending punctuation followed by space or newline
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    return [s.strip() for s in sentences if s.strip()]


def generate_audio_with_espeak(text, output_file, voice="en-us", speed=145):
    """Generate audio using espeak-ng command line."""
    # espeak-ng speed is words per minute
    cmd = [
        "espeak-ng",
        "-v", voice,
        "-s", str(speed),
        "-w", output_file,
        text
    ]
    subprocess.run(cmd, check=True, capture_output=True)


def generate_audio_and_timestamps():
    """Generate audio using espeak-ng and create timestamp file."""
    
    print("Initializing TTS engine with espeak-ng (en-us voice)...")
    
    # Output paths - use script directory
    output_dir = os.path.dirname(os.path.abspath(__file__))
    temp_wav_files = []
    timestamps = []
    current_time = 0.0
    
    print("\nGenerating audio for each section...")
    
    for i, section_data in enumerate(SCRIPT_SECTIONS):
        section_name = section_data["section"]
        text = section_data["text"]
        
        print(f"  Processing section {i+1}/{len(SCRIPT_SECTIONS)}: {section_name}")
        
        section_start = current_time
        sentences = split_into_sentences(text)
        sentence_timestamps = []
        
        # Generate audio for this section
        temp_file = f"/tmp/section_{i}.wav"
        temp_wav_files.append(temp_file)
        
        # Use espeak-ng directly
        generate_audio_with_espeak(text, temp_file, voice="en-us", speed=145)
        
        # Get actual duration from the generated file
        with wave.open(temp_file, 'rb') as wf:
            frames = wf.getnframes()
            rate = wf.getframerate()
            section_duration = frames / float(rate)
        
        # Estimate sentence timestamps based on character count
        total_chars = sum(len(s) for s in sentences)
        
        sentence_start = current_time
        for j, sentence in enumerate(sentences):
            sentence_ratio = len(sentence) / total_chars if total_chars > 0 else 0
            sentence_duration = section_duration * sentence_ratio
            
            sentence_timestamps.append({
                "sentence_index": j,
                "text": sentence,
                "start_time": round(sentence_start, 3),
                "end_time": round(sentence_start + sentence_duration, 3),
                "duration": round(sentence_duration, 3)
            })
            
            sentence_start += sentence_duration
        
        current_time += section_duration
        
        # Add pause between sections
        pause_duration = 0.5
        current_time += pause_duration
        
        # Store section-level timestamp
        timestamps.append({
            "section": section_name,
            "section_index": i,
            "start_time": round(section_start, 3),
            "end_time": round(section_start + section_duration, 3),
            "duration": round(section_duration, 3),
            "sentences": sentence_timestamps
        })
        
        print(f"    Duration: {section_duration:.2f}s")
    
    # Combine all audio files into one
    print("\nCombining audio segments...")
    output_audio_path = os.path.join(output_dir, "binary_search_narration.wav")
    
    combined_audio = []
    sample_rate = None
    sample_width = None
    num_channels = None
    
    for temp_file in temp_wav_files:
        with wave.open(temp_file, 'rb') as wf:
            if sample_rate is None:
                sample_rate = wf.getframerate()
                sample_width = wf.getsampwidth()
                num_channels = wf.getnchannels()
            
            frames = wf.readframes(wf.getnframes())
            combined_audio.append(frames)
            
            # Add 0.5 second pause between sections
            pause_samples = int(0.5 * sample_rate * num_channels)
            pause_bytes = b'\x00' * (pause_samples * sample_width)
            combined_audio.append(pause_bytes)
    
    # Write combined audio
    with wave.open(output_audio_path, 'wb') as wf:
        wf.setnchannels(num_channels)
        wf.setsampwidth(sample_width)
        wf.setframerate(sample_rate)
        wf.writeframes(b''.join(combined_audio))
    
    # Calculate total duration
    with wave.open(output_audio_path, 'rb') as wf:
        total_frames = wf.getnframes()
        total_duration = total_frames / float(wf.getframerate())
    
    # Clean up temp files
    for temp_file in temp_wav_files:
        if os.path.exists(temp_file):
            os.remove(temp_file)
    
    # Create timestamp data structure
    timestamp_data = {
        "metadata": {
            "title": "How Binary Search Actually Works - Visualized",
            "voice": "espeak-ng (en-us) - Placeholder for Kokoro af_bella",
            "target_voice": "kokoro/af_bella",
            "language": "en-US",
            "sample_rate": sample_rate,
            "total_duration_seconds": round(total_duration, 3),
            "total_duration_formatted": f"{int(total_duration // 60)}:{int(total_duration % 60):02d}",
            "audio_file": "binary_search_narration.wav",
            "note": "Timestamps are designed for Kokoro TTS af_bella voice. Current audio uses espeak-ng as fallback due to network restrictions. Re-run with Kokoro locally for production quality."
        },
        "sections": timestamps
    }
    
    # Save timestamp file
    output_timestamp_path = os.path.join(output_dir, "binary_search_timestamps.json")
    print(f"Saving timestamps to: {output_timestamp_path}")
    with open(output_timestamp_path, 'w', encoding='utf-8') as f:
        json.dump(timestamp_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n✓ Audio generation complete!")
    print(f"  Total duration: {total_duration:.2f} seconds ({total_duration/60:.1f} minutes)")
    print(f"  Audio file: {output_audio_path}")
    print(f"  Timestamp file: {output_timestamp_path}")
    
    return output_audio_path, output_timestamp_path


if __name__ == "__main__":
    generate_audio_and_timestamps()
