"""
Binary Search Visualization - Professional Manim Animation
============================================================
How Binary Search Actually Works - Visualized

Target: 1920x1080 @ 60fps
Duration: ~9:37 (577 seconds)
Style: 3Blue1Brown inspired, professional, smooth animations

Based on:
- binary_search_script.md (narration)
- binary_search_timestamps.json (timing)
- binary_search_visual_description.md (visual guide)
- coding_visuals_tips_and_methods.txt (best practices)
"""

from manim import *
import numpy as np

# =============================================================================
# DESIGN CONSTANTS - Following 8pt Grid System
# =============================================================================

# Color Semantic System
ARRAY_BG_COLOR = "#1a1a2e"
ELEMENT_DEFAULT = BLUE_C
ELEMENT_CHECKED = YELLOW
ELEMENT_ELIMINATED = "#4a4a4a"  # Dark gray
ELEMENT_FOUND = GREEN
LEFT_POINTER_COLOR = RED_B
RIGHT_POINTER_COLOR = GREEN_B
MID_POINTER_COLOR = YELLOW
TARGET_COLOR = GOLD
ACCENT_COLOR = "#e94560"
BG_COLOR = "#0f0f23"

# Layout Constants (8pt Grid)
BASE_UNIT = 0.5
ARRAY_ELEMENT_WIDTH = 0.75
ARRAY_ELEMENT_HEIGHT = 0.75
ELEMENT_SPACING = 0.1
SECTION_SPACING = 1.0
POINTER_OFFSET = 0.5

# Typography Hierarchy
TITLE_SCALE = 1.2
SUBTITLE_SCALE = 0.8
LABEL_SCALE = 0.5
CODE_SCALE = 0.45
SMALL_LABEL_SCALE = 0.4

# Animation Timing
FAST = 0.3
MEDIUM = 0.6
SLOW = 1.0
VERY_SLOW = 1.5


# =============================================================================
# REUSABLE COMPONENTS
# =============================================================================

class ArrayElement(VGroup):
    """A single array element with value and optional index label."""
    
    def __init__(self, value, index=None, width=ARRAY_ELEMENT_WIDTH, 
                 height=ARRAY_ELEMENT_HEIGHT, color=ELEMENT_DEFAULT, **kwargs):
        super().__init__(**kwargs)
        
        # Background rectangle
        self.bg = RoundedRectangle(
            width=width, height=height,
            corner_radius=0.1,
            fill_color=color,
            fill_opacity=0.3,
            stroke_color=color,
            stroke_width=2
        )
        
        # Value text
        self.value_text = Text(str(value), font_size=24).move_to(self.bg)
        
        self.add(self.bg, self.value_text)
        
        # Optional index label
        if index is not None:
            self.index_label = Text(str(index), font_size=16, color=GRAY)
            self.index_label.next_to(self.bg, DOWN, buff=0.15)
            self.add(self.index_label)
        
        self.value = value
    
    def set_state(self, state):
        """Change element state: 'default', 'checked', 'eliminated', 'found'"""
        colors = {
            'default': ELEMENT_DEFAULT,
            'checked': ELEMENT_CHECKED,
            'eliminated': ELEMENT_ELIMINATED,
            'found': ELEMENT_FOUND
        }
        color = colors.get(state, ELEMENT_DEFAULT)
        self.bg.set_fill(color, opacity=0.3 if state != 'eliminated' else 0.1)
        self.bg.set_stroke(color)
        if state == 'eliminated':
            self.value_text.set_opacity(0.3)


class ArrayVisualization(VGroup):
    """A complete array visualization with elements."""
    
    def __init__(self, values, show_indices=True, **kwargs):
        super().__init__(**kwargs)
        self.elements = []
        
        for i, val in enumerate(values):
            elem = ArrayElement(val, index=i if show_indices else None)
            self.elements.append(elem)
            self.add(elem)
        
        self.arrange(RIGHT, buff=ELEMENT_SPACING)
    
    def get_element(self, index):
        return self.elements[index]
    
    def highlight_range(self, start, end, color=ELEMENT_DEFAULT):
        """Highlight a range of elements."""
        for i, elem in enumerate(self.elements):
            if start <= i <= end:
                elem.set_state('default')
            else:
                elem.set_state('eliminated')


class Pointer(VGroup):
    """A pointer arrow with label for array visualization."""
    
    def __init__(self, label_text, color, direction=DOWN, **kwargs):
        super().__init__(**kwargs)
        
        self.arrow = Arrow(
            start=ORIGIN, end=direction * 0.5,
            color=color,
            stroke_width=4,
            max_tip_length_to_length_ratio=0.4
        )
        
        self.label = Text(label_text, font_size=20, color=color)
        if direction[1] < 0:  # Pointing down
            self.label.next_to(self.arrow, UP, buff=0.1)
        else:  # Pointing up
            self.label.next_to(self.arrow, DOWN, buff=0.1)
        
        self.add(self.arrow, self.label)
    
    def point_to(self, mobject, direction=UP):
        """Position pointer above/below a mobject."""
        if direction[1] > 0:
            self.next_to(mobject, UP, buff=0.2)
        else:
            self.next_to(mobject, DOWN, buff=0.2)


# =============================================================================
# SCENE 1: INTRODUCTION
# =============================================================================

class IntroductionScene(Scene):
    """Opening scene with dictionary analogy and binary search introduction."""
    
    def construct(self):
        self.camera.background_color = BG_COLOR
        
        # Scene 1.1: Dictionary Analogy (0:00 - 16.13s)
        self.dictionary_analogy()
        
        # Scene 1.2: Smart Approach (16.13 - 36.74s)
        self.smart_approach()
        
        # Scene 1.3: Binary Search Title (36.74 - 68.92s)
        self.binary_search_intro()
    
    def dictionary_analogy(self):
        """Show dictionary and page flipping."""
        # Create dictionary visual
        dictionary_cover = RoundedRectangle(
            width=4, height=5,
            corner_radius=0.2,
            fill_color="#8B4513",
            fill_opacity=0.9,
            stroke_color="#5D3A1A",
            stroke_width=4
        )
        
        title_on_book = Text("DICTIONARY", font_size=28, color=GOLD)
        title_on_book.move_to(dictionary_cover).shift(UP * 0.5)
        
        subtitle = Text("50,000 words", font_size=18, color="#DDD")
        subtitle.next_to(title_on_book, DOWN, buff=0.3)
        
        dictionary = VGroup(dictionary_cover, title_on_book, subtitle)
        
        # Animate dictionary appearing
        self.play(FadeIn(dictionary, scale=0.8), run_time=SLOW)
        self.wait(1)
        
        # Show "flipping pages" concept
        page_text = Text("Flipping page by page...", font_size=24, color=GRAY)
        page_text.next_to(dictionary, RIGHT, buff=1)
        
        # Create pages animation
        pages = VGroup()
        for i in range(5):
            page = Rectangle(width=3.8, height=4.8, fill_color=WHITE, fill_opacity=0.9)
            page.move_to(dictionary_cover)
            pages.add(page)
        
        self.play(Write(page_text), run_time=MEDIUM)
        
        # Simulate slow page flipping
        for i in range(3):
            self.play(
                pages[i].animate.shift(LEFT * 0.3).set_opacity(0.5),
                run_time=0.8
            )
        
        # Question mark appears
        question = Text("?", font_size=72, color=ACCENT_COLOR)
        question.next_to(page_text, DOWN, buff=0.5)
        
        tedious_text = Text("Too slow!", font_size=20, color=RED)
        tedious_text.next_to(question, DOWN, buff=0.2)
        
        self.play(
            Write(question),
            FadeIn(tedious_text),
            run_time=MEDIUM
        )
        self.wait(1)
        
        # Clear for next part
        self.play(
            FadeOut(VGroup(dictionary, page_text, pages, question, tedious_text)),
            run_time=FAST
        )
    
    def smart_approach(self):
        """Show the smarter dictionary approach - opening to middle."""
        # Open book visualization
        left_page = Rectangle(width=3, height=4, fill_color=WHITE, fill_opacity=0.95)
        right_page = Rectangle(width=3, height=4, fill_color=WHITE, fill_opacity=0.95)
        
        left_page.shift(LEFT * 1.6)
        right_page.shift(RIGHT * 1.6)
        
        spine = Line(UP * 2, DOWN * 2, color="#5D3A1A", stroke_width=4)
        
        open_book = VGroup(left_page, right_page, spine)
        
        # Page content hints
        left_content = VGroup(
            Text("A - L", font_size=20, color=GRAY),
            Text("...", font_size=16, color=GRAY).shift(DOWN * 0.5)
        ).move_to(left_page)
        
        right_content = VGroup(
            Text("M - Z", font_size=20, color=GRAY),
            Text("...", font_size=16, color=GRAY).shift(DOWN * 0.5)
        ).move_to(right_page)
        
        # Middle indicator
        middle_text = Text("You are here: M", font_size=24, color=YELLOW)
        middle_text.next_to(open_book, UP, buff=0.5)
        
        self.play(FadeIn(open_book), run_time=SLOW)
        self.play(
            FadeIn(left_content),
            FadeIn(right_content),
            run_time=MEDIUM
        )
        self.play(Write(middle_text), run_time=MEDIUM)
        
        # Show decision arrows
        left_arrow = Arrow(spine.get_center(), left_page.get_center(), color=BLUE)
        right_arrow = Arrow(spine.get_center(), right_page.get_center(), color=GREEN)
        
        left_label = Text("Go back?", font_size=18, color=BLUE)
        left_label.next_to(left_arrow, DOWN, buff=0.1)
        
        right_label = Text("Go forward?", font_size=18, color=GREEN)
        right_label.next_to(right_arrow, DOWN, buff=0.1)
        
        self.play(
            GrowArrow(left_arrow),
            GrowArrow(right_arrow),
            run_time=MEDIUM
        )
        self.play(
            Write(left_label),
            Write(right_label),
            run_time=MEDIUM
        )
        
        # Highlight insight
        insight_box = RoundedRectangle(
            width=8, height=1.2,
            corner_radius=0.2,
            fill_color=ACCENT_COLOR,
            fill_opacity=0.2,
            stroke_color=ACCENT_COLOR
        ).to_edge(DOWN, buff=1)
        
        insight_text = Text(
            "One decision eliminates HALF the options!",
            font_size=24,
            color=WHITE
        ).move_to(insight_box)
        
        self.play(
            FadeIn(insight_box),
            Write(insight_text),
            run_time=SLOW
        )
        self.wait(2)
        
        # Transition out
        all_elements = VGroup(
            open_book, left_content, right_content, middle_text,
            left_arrow, right_arrow, left_label, right_label,
            insight_box, insight_text
        )
        self.play(FadeOut(all_elements), run_time=MEDIUM)
    
    def binary_search_intro(self):
        """Show the Binary Search title and concept."""
        # Main title with dramatic reveal
        title = Text("BINARY SEARCH", font_size=72, color=WHITE)
        title.set_color_by_gradient(BLUE, GREEN)
        
        subtitle = Text("Divide and Conquer", font_size=32, color=GRAY)
        subtitle.next_to(title, DOWN, buff=0.5)
        
        # Animate title
        self.play(
            Write(title, run_time=1.5),
        )
        self.play(FadeIn(subtitle, shift=UP * 0.3), run_time=MEDIUM)
        self.wait(1)
        
        # Move title up
        self.play(
            VGroup(title, subtitle).animate.to_edge(UP, buff=0.5),
            run_time=MEDIUM
        )
        
        # Show simple array demonstration
        values = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
        array = ArrayVisualization(values, show_indices=False)
        array.scale(0.9)
        
        self.play(FadeIn(array, shift=UP * 0.5), run_time=SLOW)
        self.wait(0.5)
        
        # Show splitting line
        split_line = DashedLine(
            array.get_center() + UP * 0.8,
            array.get_center() + DOWN * 0.8,
            color=YELLOW,
            dash_length=0.1
        )
        
        self.play(Create(split_line), run_time=MEDIUM)
        
        # Highlight halves
        left_half_box = SurroundingRectangle(
            VGroup(*array.elements[:5]),
            color=BLUE,
            buff=0.1
        )
        right_half_box = SurroundingRectangle(
            VGroup(*array.elements[5:]),
            color=GREEN,
            buff=0.1
        )
        
        left_label = Text("Left Half", font_size=18, color=BLUE)
        left_label.next_to(left_half_box, DOWN, buff=0.2)
        
        right_label = Text("Right Half", font_size=18, color=GREEN)
        right_label.next_to(right_half_box, DOWN, buff=0.2)
        
        self.play(
            Create(left_half_box),
            Create(right_half_box),
            run_time=MEDIUM
        )
        self.play(
            Write(left_label),
            Write(right_label),
            run_time=MEDIUM
        )
        self.wait(1)
        
        # Power teaser
        power_text = VGroup(
            Text("1,000,000 elements", font_size=28, color=WHITE),
            Text("→", font_size=28, color=YELLOW).shift(RIGHT * 3),
            Text("20 comparisons", font_size=28, color=GREEN).shift(RIGHT * 6)
        ).arrange(RIGHT, buff=0.5)
        power_text.next_to(array, DOWN, buff=1.5)
        
        self.play(Write(power_text[0]), run_time=MEDIUM)
        self.play(Write(power_text[1]), run_time=FAST)
        self.play(Write(power_text[2]), run_time=MEDIUM)
        
        # Question
        question = Text("How?", font_size=48, color=ACCENT_COLOR)
        question.next_to(power_text, DOWN, buff=0.5)
        
        self.play(Write(question), run_time=MEDIUM)
        self.wait(2)
        
        # Fade out all
        self.play(
            FadeOut(VGroup(
                title, subtitle, array, split_line,
                left_half_box, right_half_box, left_label, right_label,
                power_text, question
            )),
            run_time=MEDIUM
        )


# =============================================================================
# SCENE 2: THE PROBLEM - LINEAR SEARCH
# =============================================================================

class LinearSearchProblemScene(Scene):
    """Demonstrate the problem with linear search."""
    
    def construct(self):
        self.camera.background_color = BG_COLOR
        
        # Section title
        section_title = Text("The Problem", font_size=48, color=WHITE)
        section_title.to_edge(UP, buff=0.5)
        
        self.play(Write(section_title), run_time=MEDIUM)
        
        # Problem setup
        self.linear_search_demo(section_title)
        
        # Binary search teaser comparison
        self.comparison_teaser()
    
    def linear_search_demo(self, title):
        """Show linear search being slow."""
        # Create abstract array representation
        array_rect = RoundedRectangle(
            width=12, height=0.8,
            corner_radius=0.2,
            fill_color=BLUE_E,
            fill_opacity=0.5,
            stroke_color=BLUE_C,
            stroke_width=2
        )
        
        array_label = Text("1,000,000 sorted numbers", font_size=24)
        array_label.next_to(array_rect, DOWN, buff=0.3)
        
        array_group = VGroup(array_rect, array_label)
        array_group.shift(UP * 0.5)
        
        # Target
        target_box = RoundedRectangle(
            width=2.5, height=1,
            corner_radius=0.15,
            fill_color=TARGET_COLOR,
            fill_opacity=0.3,
            stroke_color=TARGET_COLOR
        )
        target_text = Text("target = 42", font_size=20, color=TARGET_COLOR)
        target_text.move_to(target_box)
        target_group = VGroup(target_box, target_text)
        target_group.next_to(array_group, RIGHT, buff=1)
        
        self.play(
            FadeIn(array_group),
            FadeIn(target_group),
            run_time=MEDIUM
        )
        
        # Linear search animation
        linear_title = Text("Linear Search", font_size=32, color=RED)
        linear_title.next_to(title, DOWN, buff=0.3)
        
        self.play(Write(linear_title), run_time=MEDIUM)
        
        # Progress indicator
        progress_bg = RoundedRectangle(
            width=10, height=0.4,
            corner_radius=0.1,
            fill_color=GRAY,
            fill_opacity=0.3,
            stroke_color=GRAY
        )
        progress_bg.next_to(array_rect, DOWN, buff=1)
        
        progress_fill = RoundedRectangle(
            width=0.1, height=0.35,
            corner_radius=0.1,
            fill_color=RED,
            fill_opacity=0.8,
            stroke_width=0
        )
        progress_fill.align_to(progress_bg, LEFT).shift(RIGHT * 0.05)
        
        # Counter
        counter = Integer(0, font_size=36, color=WHITE)
        counter_label = Text("comparisons", font_size=20, color=GRAY)
        counter_group = VGroup(counter, counter_label).arrange(DOWN, buff=0.2)
        counter_group.next_to(progress_bg, DOWN, buff=0.5)
        
        self.play(
            FadeIn(progress_bg),
            FadeIn(progress_fill),
            FadeIn(counter_group),
            run_time=MEDIUM
        )
        
        # Animate linear scan
        def update_counter(mob, dt):
            mob.set_value(int(mob.get_value() + 50000 * dt))
        
        counter.add_updater(update_counter)
        
        self.play(
            progress_fill.animate.stretch_to_fit_width(9.9),
            run_time=3
        )
        
        counter.remove_updater(update_counter)
        counter.set_value(1000000)
        
        # Show the problem
        problem_text = Text(
            "Worst case: Check ALL 1,000,000 elements!",
            font_size=24,
            color=RED
        )
        problem_text.next_to(counter_group, DOWN, buff=0.5)
        
        self.play(Write(problem_text), run_time=MEDIUM)
        self.wait(1)
        
        # Scale up problem
        scale_texts = VGroup(
            Text("1 billion entries?", font_size=24, color=YELLOW),
            Text("10 billion?", font_size=24, color=ORANGE),
            Text("1000x per second?", font_size=24, color=RED),
        ).arrange(DOWN, buff=0.3)
        scale_texts.next_to(problem_text, DOWN, buff=0.5)
        
        for text in scale_texts:
            self.play(Write(text), run_time=0.5)
        
        self.wait(1)
        
        # Store for comparison
        self.linear_elements = VGroup(
            array_group, target_group, linear_title,
            progress_bg, progress_fill, counter_group,
            problem_text, scale_texts
        )
        
        # Clear for comparison
        self.play(FadeOut(self.linear_elements), run_time=MEDIUM)
    
    def comparison_teaser(self):
        """Show the dramatic comparison."""
        # Split screen setup
        divider = Line(UP * 3.5, DOWN * 2.5, color=WHITE, stroke_width=2)
        
        # Left side - Linear
        linear_title = Text("LINEAR", font_size=36, color=RED)
        linear_title.move_to(LEFT * 3.5 + UP * 2.5)
        
        linear_count = Text("1,000,000", font_size=64, color=RED)
        linear_count.move_to(LEFT * 3.5)
        
        linear_label = Text("comparisons", font_size=24, color=GRAY)
        linear_label.next_to(linear_count, DOWN, buff=0.2)
        
        linear_x = Cross(stroke_color=RED, stroke_width=8).scale(0.5)
        linear_x.next_to(linear_label, DOWN, buff=0.5)
        
        # Right side - Binary
        binary_title = Text("BINARY", font_size=36, color=GREEN)
        binary_title.move_to(RIGHT * 3.5 + UP * 2.5)
        
        binary_count = Text("20", font_size=96, color=GREEN)
        binary_count.move_to(RIGHT * 3.5)
        
        binary_label = Text("comparisons", font_size=24, color=GRAY)
        binary_label.next_to(binary_count, DOWN, buff=0.2)
        
        binary_check = Text("✓", font_size=64, color=GREEN)
        binary_check.next_to(binary_label, DOWN, buff=0.5)
        
        # Animate comparison
        self.play(Create(divider), run_time=MEDIUM)
        
        self.play(
            Write(linear_title),
            Write(binary_title),
            run_time=MEDIUM
        )
        
        self.play(
            Write(linear_count),
            Write(linear_label),
            run_time=MEDIUM
        )
        
        # Dramatic reveal of 20
        self.play(
            Write(binary_count, run_time=1.5),
            Write(binary_label),
        )
        
        self.play(
            FadeIn(linear_x),
            Write(binary_check),
            run_time=MEDIUM
        )
        
        # Emphasis
        emphasis_box = SurroundingRectangle(
            binary_count, color=GREEN, buff=0.3
        )
        self.play(Create(emphasis_box), run_time=MEDIUM)
        
        # Question
        question = Text("How is this possible?", font_size=36, color=YELLOW)
        question.to_edge(DOWN, buff=1)
        
        self.play(Write(question), run_time=MEDIUM)
        self.wait(2)
        
        # Fade out
        self.play(
            FadeOut(VGroup(
                divider, linear_title, linear_count, linear_label, linear_x,
                binary_title, binary_count, binary_label, binary_check,
                emphasis_box, question
            )),
            run_time=MEDIUM
        )


# =============================================================================
# SCENE 3: THE CORE INSIGHT - POWER OF HALVING
# =============================================================================

class CoreInsightScene(Scene):
    """Demonstrate the power of halving."""
    
    def construct(self):
        self.camera.background_color = BG_COLOR
        
        # Section title
        title = Text("The Core Insight", font_size=48, color=WHITE)
        title.to_edge(UP, buff=0.5)
        
        self.play(Write(title), run_time=MEDIUM)
        
        # Main demonstration
        self.halving_demonstration(title)
        
        # Million to one progression
        self.million_to_one()
    
    def halving_demonstration(self, title):
        """Show how one comparison eliminates half."""
        # Key insight text
        insight = Text(
            "One comparison eliminates HALF",
            font_size=32,
            color=YELLOW
        )
        insight.next_to(title, DOWN, buff=0.5)
        
        self.play(Write(insight), run_time=MEDIUM)
        
        # Create array
        values = [2, 5, 8, 11, 15, 18, 23, 27, 31, 35]
        array = ArrayVisualization(values, show_indices=True)
        array.scale(0.8)
        array.next_to(insight, DOWN, buff=1)
        
        self.play(FadeIn(array), run_time=MEDIUM)
        
        # Show target
        target_val = 8
        target_box = VGroup(
            RoundedRectangle(
                width=2, height=0.8,
                corner_radius=0.1,
                fill_color=TARGET_COLOR,
                fill_opacity=0.3,
                stroke_color=TARGET_COLOR
            ),
            Text(f"target = {target_val}", font_size=20, color=TARGET_COLOR)
        )
        target_box[1].move_to(target_box[0])
        target_box.next_to(array, RIGHT, buff=1)
        
        self.play(FadeIn(target_box), run_time=MEDIUM)
        
        # Point to middle
        mid_idx = len(values) // 2
        mid_elem = array.get_element(mid_idx)
        
        mid_pointer = Pointer("mid", MID_POINTER_COLOR)
        mid_pointer.next_to(mid_elem, UP, buff=0.3)
        
        self.play(FadeIn(mid_pointer), run_time=MEDIUM)
        
        # Comparison
        comparison_text = MathTex(
            f"{target_val}", "<", f"{values[mid_idx]}",
            font_size=36
        )
        comparison_text[0].set_color(TARGET_COLOR)
        comparison_text[2].set_color(MID_POINTER_COLOR)
        comparison_text.next_to(array, DOWN, buff=1)
        
        self.play(Write(comparison_text), run_time=MEDIUM)
        self.wait(0.5)
        
        # Eliminate right half
        eliminate_text = Text("Eliminate right half!", font_size=24, color=RED)
        eliminate_text.next_to(comparison_text, DOWN, buff=0.3)
        
        self.play(Write(eliminate_text), run_time=MEDIUM)
        
        # Fade right half
        for i in range(mid_idx, len(values)):
            array.elements[i].set_state('eliminated')
        
        self.play(
            *[array.elements[i].animate.set_opacity(0.3) 
              for i in range(mid_idx, len(values))],
            run_time=MEDIUM
        )
        
        # Highlight remaining
        remaining_box = SurroundingRectangle(
            VGroup(*array.elements[:mid_idx]),
            color=GREEN,
            buff=0.15
        )
        
        remaining_text = Text(
            f"Only {mid_idx} elements left!",
            font_size=24,
            color=GREEN
        )
        remaining_text.next_to(eliminate_text, DOWN, buff=0.3)
        
        self.play(
            Create(remaining_box),
            Write(remaining_text),
            run_time=MEDIUM
        )
        
        self.wait(2)
        
        # Clear for next part
        self.play(
            FadeOut(VGroup(
                insight, array, target_box, mid_pointer,
                comparison_text, eliminate_text, remaining_box, remaining_text
            )),
            run_time=MEDIUM
        )
    
    def million_to_one(self):
        """Show the progression from 1M to 1."""
        # Build progression table
        progression_title = Text(
            "Million to One",
            font_size=36,
            color=WHITE
        )
        progression_title.to_edge(UP, buff=1.5)
        
        self.play(Write(progression_title), run_time=MEDIUM)
        
        # Create rows
        rows = []
        comparisons = [1, 2, 5, 10, 15, 20]
        elements = [500000, 250000, 31250, 977, 31, 1]
        
        for i, (comp, elem) in enumerate(zip(comparisons, elements)):
            comp_text = Text(f"After {comp}:", font_size=22, color=GRAY)
            elem_text = Text(f"{elem:,}", font_size=22, color=GREEN)
            
            row = VGroup(comp_text, elem_text).arrange(RIGHT, buff=1)
            rows.append(row)
        
        table = VGroup(*rows).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        table.next_to(progression_title, DOWN, buff=0.5)
        
        # Animate rows appearing
        for row in rows:
            self.play(FadeIn(row, shift=LEFT * 0.3), run_time=0.4)
        
        # Highlight final
        final_box = SurroundingRectangle(rows[-1], color=GREEN, buff=0.1)
        self.play(Create(final_box), run_time=MEDIUM)
        
        # Show logarithmic text
        log_text = MathTex(
            r"\log_2(1{,}000{,}000) \approx 20",
            font_size=36
        )
        log_text.set_color(YELLOW)
        log_text.next_to(table, DOWN, buff=1)
        
        self.play(Write(log_text), run_time=MEDIUM)
        
        # Logarithmic behavior label
        behavior_text = Text(
            "This is logarithmic behavior!",
            font_size=28,
            color=ACCENT_COLOR
        )
        behavior_text.next_to(log_text, DOWN, buff=0.5)
        
        self.play(Write(behavior_text), run_time=MEDIUM)
        
        self.wait(2)
        
        # Fade out
        self.play(
            FadeOut(VGroup(
                progression_title, table, final_box, log_text, behavior_text
            )),
            run_time=MEDIUM
        )


# =============================================================================
# SCENE 4: THE ALGORITHM IN ACTION
# =============================================================================

class AlgorithmInActionScene(Scene):
    """Show the binary search algorithm step by step."""
    
    def construct(self):
        self.camera.background_color = BG_COLOR
        
        # Title
        title = Text("The Algorithm in Action", font_size=42, color=WHITE)
        title.to_edge(UP, buff=0.5)
        
        self.play(Write(title), run_time=MEDIUM)
        
        # Run algorithm demonstration
        self.algorithm_demo()
    
    def algorithm_demo(self):
        """Demonstrate binary search step by step."""
        # Create array
        values = [2, 5, 8, 11, 15, 18, 23, 27, 31, 35]
        target = 23
        
        array = ArrayVisualization(values, show_indices=True)
        array.scale(0.75)
        array.shift(UP * 0.5)
        
        self.play(FadeIn(array), run_time=MEDIUM)
        
        # Target display
        target_display = VGroup(
            Text("Target:", font_size=24, color=GRAY),
            Text(str(target), font_size=32, color=TARGET_COLOR)
        ).arrange(RIGHT, buff=0.3)
        target_display.to_edge(RIGHT, buff=1).shift(UP * 2)
        
        self.play(FadeIn(target_display), run_time=MEDIUM)
        
        # Create pointers
        left_pointer = Pointer("L", LEFT_POINTER_COLOR)
        right_pointer = Pointer("R", RIGHT_POINTER_COLOR)
        mid_pointer = Pointer("mid", MID_POINTER_COLOR)
        
        # Initialize pointers
        left = 0
        right = len(values) - 1
        
        left_pointer.next_to(array.elements[left], UP, buff=0.3)
        right_pointer.next_to(array.elements[right], UP, buff=0.3)
        
        self.play(
            FadeIn(left_pointer),
            FadeIn(right_pointer),
            run_time=MEDIUM
        )
        
        # Status text area
        status_area = VGroup()
        
        # Algorithm loop
        iteration = 0
        found = False
        
        while left <= right and not found:
            iteration += 1
            mid = left + (right - left) // 2
            
            # Move mid pointer
            mid_pointer.next_to(array.elements[mid], UP, buff=0.3)
            
            if iteration == 1:
                self.play(FadeIn(mid_pointer), run_time=MEDIUM)
            else:
                self.play(
                    mid_pointer.animate.next_to(array.elements[mid], UP, buff=0.3),
                    run_time=MEDIUM
                )
            
            # Highlight current element
            array.elements[mid].bg.set_stroke(YELLOW, width=4)
            self.wait(0.3)
            
            # Show comparison
            mid_val = values[mid]
            
            if mid_val == target:
                # Found!
                found = True
                
                status = Text(
                    f"Found! {mid_val} = {target}",
                    font_size=24,
                    color=GREEN
                )
                status.next_to(array, DOWN, buff=1)
                
                self.play(Write(status), run_time=MEDIUM)
                
                # Celebrate
                array.elements[mid].set_state('found')
                self.play(
                    array.elements[mid].animate.scale(1.2),
                    run_time=MEDIUM
                )
                
                found_label = Text("✓ FOUND", font_size=36, color=GREEN)
                found_label.next_to(array.elements[mid], DOWN, buff=0.8)
                
                self.play(Write(found_label), run_time=MEDIUM)
                
            elif mid_val < target:
                # Go right
                status = Text(
                    f"{mid_val} < {target} → Go RIGHT",
                    font_size=24,
                    color=GREEN
                )
                status.next_to(array, DOWN, buff=1)
                
                self.play(Write(status), run_time=MEDIUM)
                
                # Eliminate left half
                for i in range(left, mid + 1):
                    array.elements[i].set_state('eliminated')
                
                self.play(
                    *[array.elements[i].animate.set_opacity(0.3) 
                      for i in range(left, mid + 1)],
                    run_time=MEDIUM
                )
                
                left = mid + 1
                
                # Move left pointer
                if left <= right:
                    self.play(
                        left_pointer.animate.next_to(
                            array.elements[left], UP, buff=0.3
                        ),
                        FadeOut(status),
                        run_time=MEDIUM
                    )
                
            else:
                # Go left
                status = Text(
                    f"{mid_val} > {target} → Go LEFT",
                    font_size=24,
                    color=BLUE
                )
                status.next_to(array, DOWN, buff=1)
                
                self.play(Write(status), run_time=MEDIUM)
                
                # Eliminate right half
                for i in range(mid, right + 1):
                    array.elements[i].set_state('eliminated')
                
                self.play(
                    *[array.elements[i].animate.set_opacity(0.3) 
                      for i in range(mid, right + 1)],
                    run_time=MEDIUM
                )
                
                right = mid - 1
                
                # Move right pointer
                if left <= right:
                    self.play(
                        right_pointer.animate.next_to(
                            array.elements[right], UP, buff=0.3
                        ),
                        FadeOut(status),
                        run_time=MEDIUM
                    )
            
            # Reset current element highlight
            if not found:
                array.elements[mid].bg.set_stroke(ELEMENT_ELIMINATED, width=2)
            
            self.wait(0.5)
        
        # Elegance message
        elegance = Text(
            "Each comparison: Maximum information. Nothing wasted.",
            font_size=24,
            color=GRAY
        )
        elegance.to_edge(DOWN, buff=1)
        
        self.play(Write(elegance), run_time=MEDIUM)
        self.wait(2)


# =============================================================================
# SCENE 5: THE MATHEMATICS
# =============================================================================

class MathematicsScene(Scene):
    """Explain the logarithmic mathematics."""
    
    def construct(self):
        self.camera.background_color = BG_COLOR
        
        title = Text("The Mathematics", font_size=48, color=WHITE)
        title.to_edge(UP, buff=0.5)
        
        self.play(Write(title), run_time=MEDIUM)
        
        # Formula derivation
        self.formula_derivation()
        
        # Complexity comparison graph
        self.complexity_graph()
    
    def formula_derivation(self):
        """Show the logarithmic formula derivation."""
        # Step by step
        steps = [
            MathTex(r"\text{Start: } n \text{ elements}"),
            MathTex(r"\text{After 1 step: } \frac{n}{2}"),
            MathTex(r"\text{After 2 steps: } \frac{n}{4} = \frac{n}{2^2}"),
            MathTex(r"\text{After } k \text{ steps: } \frac{n}{2^k}"),
        ]
        
        for step in steps:
            step.scale(0.9)
        
        steps_group = VGroup(*steps).arrange(DOWN, buff=0.5, aligned_edge=LEFT)
        steps_group.shift(UP * 0.5)
        
        for step in steps:
            self.play(Write(step), run_time=0.8)
            self.wait(0.3)
        
        self.wait(1)
        
        # Key equation
        key_eq = MathTex(
            r"\text{When } \frac{n}{2^k} = 1 \text{, we find: } k = \log_2(n)",
            font_size=36
        )
        key_eq.set_color(YELLOW)
        key_eq.next_to(steps_group, DOWN, buff=1)
        
        key_box = SurroundingRectangle(key_eq, color=YELLOW, buff=0.2)
        
        self.play(
            Write(key_eq),
            Create(key_box),
            run_time=SLOW
        )
        
        # Concrete examples
        examples = VGroup(
            Text("n = 1,000,000  →  k ≈ 20", font_size=24),
            Text("n = 1,000,000,000  →  k ≈ 30", font_size=24),
            Text("n = 1,000,000,000,000  →  k ≈ 40", font_size=24),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        examples.next_to(key_box, DOWN, buff=0.8)
        
        for example in examples:
            self.play(Write(example), run_time=0.5)
        
        self.wait(2)
        
        # Clear for graph
        self.play(
            FadeOut(VGroup(steps_group, key_eq, key_box, examples)),
            run_time=MEDIUM
        )
    
    def complexity_graph(self):
        """Show O(n) vs O(log n) graph."""
        # Create axes
        axes = Axes(
            x_range=[0, 100, 20],
            y_range=[0, 100, 20],
            x_length=8,
            y_length=5,
            axis_config={"color": WHITE},
            x_axis_config={"numbers_to_include": [20, 40, 60, 80, 100]},
            y_axis_config={"numbers_to_include": [20, 40, 60, 80, 100]},
        )
        
        # Labels
        x_label = Text("Input Size", font_size=20)
        x_label.next_to(axes.x_axis, DOWN, buff=0.5)
        
        y_label = Text("Comparisons", font_size=20)
        y_label.next_to(axes.y_axis, LEFT, buff=0.5).rotate(PI/2)
        
        axes_group = VGroup(axes, x_label, y_label)
        axes_group.shift(DOWN * 0.5)
        
        self.play(Create(axes), Write(x_label), Write(y_label), run_time=SLOW)
        
        # Linear function O(n)
        linear_graph = axes.plot(
            lambda x: x,
            x_range=[0, 100],
            color=RED
        )
        linear_label = Text("O(n) - Linear", font_size=20, color=RED)
        linear_label.next_to(axes, UP, buff=0.3).shift(LEFT * 2)
        
        # Logarithmic function O(log n) - scaled for visibility
        log_graph = axes.plot(
            lambda x: np.log2(x + 1) * 15 if x > 0 else 0,
            x_range=[0.1, 100],
            color=GREEN
        )
        log_label = Text("O(log n) - Binary Search", font_size=20, color=GREEN)
        log_label.next_to(linear_label, DOWN, buff=0.2, aligned_edge=LEFT)
        
        # Animate graphs
        self.play(
            Create(linear_graph),
            Write(linear_label),
            run_time=SLOW
        )
        
        self.play(
            Create(log_graph),
            Write(log_label),
            run_time=SLOW
        )
        
        # Highlight difference
        diff_arrow = Arrow(
            axes.c2p(80, 80),
            axes.c2p(80, np.log2(81) * 15),
            color=YELLOW,
            stroke_width=3
        )
        diff_label = Text("HUGE\ndifference!", font_size=18, color=YELLOW)
        diff_label.next_to(diff_arrow, RIGHT, buff=0.2)
        
        self.play(
            GrowArrow(diff_arrow),
            Write(diff_label),
            run_time=MEDIUM
        )
        
        # Quote comparison
        quote_linear = Text(
            '"2× data = 2× time"',
            font_size=20,
            color=RED
        )
        quote_binary = Text(
            '"2× data = +1 comparison"',
            font_size=20,
            color=GREEN
        )
        
        quotes = VGroup(quote_linear, quote_binary).arrange(DOWN, buff=0.3)
        quotes.to_edge(RIGHT, buff=0.5)
        
        self.play(Write(quote_linear), run_time=MEDIUM)
        self.play(Write(quote_binary), run_time=MEDIUM)
        
        self.wait(2)


# =============================================================================
# SCENE 6: COMMON PITFALLS
# =============================================================================

class CommonPitfallsScene(Scene):
    """Highlight common implementation mistakes."""
    
    def construct(self):
        self.camera.background_color = BG_COLOR
        
        title = Text("Common Pitfalls", font_size=48, color=WHITE)
        title.to_edge(UP, buff=0.5)
        
        self.play(Write(title), run_time=MEDIUM)
        
        # Pitfall 1: Middle index overflow
        self.middle_overflow()
        
        # Pitfall 2: Boundary updates
        self.boundary_updates()
        
        # Advice
        self.advice()
    
    def middle_overflow(self):
        """Show the middle index overflow problem."""
        pitfall_title = Text("1. Middle Index Calculation", font_size=28, color=YELLOW)
        pitfall_title.next_to(self.mobjects[0], DOWN, buff=0.5).to_edge(LEFT, buff=1)
        
        self.play(Write(pitfall_title), run_time=MEDIUM)
        
        # Wrong code
        wrong_code = Code(
            code="mid = (left + right) / 2  # WRONG!",
            language="python",
            font_size=20,
            background="rectangle",
            background_stroke_color=RED
        )
        wrong_code.next_to(pitfall_title, DOWN, buff=0.5)
        
        wrong_label = Text("Can overflow!", font_size=18, color=RED)
        wrong_label.next_to(wrong_code, RIGHT, buff=0.3)
        
        self.play(FadeIn(wrong_code), Write(wrong_label), run_time=MEDIUM)
        
        # Right code
        right_code = Code(
            code="mid = left + (right - left) // 2  # CORRECT",
            language="python",
            font_size=20,
            background="rectangle",
            background_stroke_color=GREEN
        )
        right_code.next_to(wrong_code, DOWN, buff=0.5)
        
        right_label = Text("Safe!", font_size=18, color=GREEN)
        right_label.next_to(right_code, RIGHT, buff=0.3)
        
        self.play(FadeIn(right_code), Write(right_label), run_time=MEDIUM)
        
        self.wait(1.5)
        
        # Clear
        self.play(
            FadeOut(VGroup(pitfall_title, wrong_code, wrong_label, right_code, right_label)),
            run_time=MEDIUM
        )
    
    def boundary_updates(self):
        """Show boundary update pitfalls."""
        pitfall_title = Text("2. Boundary Updates", font_size=28, color=YELLOW)
        pitfall_title.next_to(self.mobjects[0], DOWN, buff=0.5).to_edge(LEFT, buff=1)
        
        self.play(Write(pitfall_title), run_time=MEDIUM)
        
        # Options
        options = VGroup(
            Text("right = mid  OR  right = mid - 1 ?", font_size=22),
            Text("left = mid  OR  left = mid + 1 ?", font_size=22),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        options.next_to(pitfall_title, DOWN, buff=0.5)
        
        self.play(Write(options), run_time=MEDIUM)
        
        # Dangers
        dangers = VGroup(
            Text("❌ Wrong choice → Infinite loop", font_size=20, color=RED),
            Text("❌ Off-by-one → Skip target", font_size=20, color=RED),
        ).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        dangers.next_to(options, DOWN, buff=0.5)
        
        for danger in dangers:
            self.play(Write(danger), run_time=0.5)
        
        self.wait(1)
        
        # Clear
        self.play(
            FadeOut(VGroup(pitfall_title, options, dangers)),
            run_time=MEDIUM
        )
    
    def advice(self):
        """Give closing advice."""
        # Statistics
        stat = Text(
            "Studies show: Most programmers get binary search wrong\non their first attempt!",
            font_size=24,
            color=ORANGE
        )
        stat.shift(UP * 0.5)
        
        self.play(Write(stat), run_time=SLOW)
        self.wait(1)
        
        # Advice box
        advice_box = RoundedRectangle(
            width=10, height=2,
            corner_radius=0.2,
            fill_color=GREEN,
            fill_opacity=0.2,
            stroke_color=GREEN
        )
        advice_box.next_to(stat, DOWN, buff=0.8)
        
        advice_items = VGroup(
            Text("✓ Test carefully", font_size=22, color=WHITE),
            Text("✓ Think through edge cases", font_size=22, color=WHITE),
            Text("✓ Trace through logic step by step", font_size=22, color=WHITE),
        ).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        advice_items.move_to(advice_box)
        
        self.play(FadeIn(advice_box), run_time=MEDIUM)
        
        for item in advice_items:
            self.play(Write(item), run_time=0.5)
        
        self.wait(2)


# =============================================================================
# SCENE 7: BEYOND SEARCHING
# =============================================================================

class BeyondSearchingScene(Scene):
    """Show applications beyond simple searching."""
    
    def construct(self):
        self.camera.background_color = BG_COLOR
        
        title = Text("Beyond Searching", font_size=48, color=WHITE)
        title.to_edge(UP, buff=0.5)
        
        self.play(Write(title), run_time=MEDIUM)
        
        # Core principle
        principle = Text(
            "The Principle: Eliminate half with each step",
            font_size=28,
            color=YELLOW
        )
        principle.next_to(title, DOWN, buff=0.5)
        
        self.play(Write(principle), run_time=MEDIUM)
        
        # Applications mind map
        central = Circle(radius=1, color=ACCENT_COLOR, fill_opacity=0.3)
        central_text = Text("Binary\nSearch", font_size=20, color=WHITE)
        central_text.move_to(central)
        central_group = VGroup(central, central_text)
        
        self.play(FadeIn(central_group), run_time=MEDIUM)
        
        # Applications
        applications = [
            ("Bisection\nMethod", BLUE, LEFT * 4 + UP * 1.5),
            ("Git\nBisect", GREEN, LEFT * 4 + DOWN * 1.5),
            ("Optimization", ORANGE, RIGHT * 4 + UP * 1.5),
            ("Machine\nLearning", PURPLE, RIGHT * 4 + DOWN * 1.5),
        ]
        
        app_groups = []
        for name, color, position in applications:
            circle = Circle(radius=0.8, color=color, fill_opacity=0.2)
            text = Text(name, font_size=16, color=WHITE)
            text.move_to(circle)
            group = VGroup(circle, text)
            group.move_to(position)
            
            # Connection line
            line = DashedLine(
                central.get_center(),
                circle.get_center(),
                color=color,
                dash_length=0.1
            )
            
            app_groups.append((group, line))
        
        for group, line in app_groups:
            self.play(
                Create(line),
                FadeIn(group),
                run_time=0.6
            )
        
        self.wait(1)
        
        # Philosophical conclusion
        conclusion = Text(
            "Not just an algorithm — A way of thinking",
            font_size=28,
            color=WHITE
        )
        conclusion.to_edge(DOWN, buff=1)
        
        self.play(Write(conclusion), run_time=MEDIUM)
        
        self.wait(2)


# =============================================================================
# SCENE 8: CLOSING
# =============================================================================

class ClosingScene(Scene):
    """Final message and end card."""
    
    def construct(self):
        self.camera.background_color = BG_COLOR
        
        # Callback to dictionary
        callback = Text(
            "Remember the dictionary?",
            font_size=32,
            color=GRAY
        )
        callback.shift(UP * 2)
        
        self.play(Write(callback), run_time=MEDIUM)
        self.wait(1)
        
        # Power statement
        power_statements = VGroup(
            Text("Millions → Twenty", font_size=36, color=GREEN),
            Text("Linear slogs → Logarithmic leaps", font_size=28, color=YELLOW),
        ).arrange(DOWN, buff=0.5)
        
        self.play(
            FadeOut(callback),
            Write(power_statements),
            run_time=SLOW
        )
        
        self.wait(2)
        
        # Final quote
        self.play(FadeOut(power_statements), run_time=MEDIUM)
        
        quote = Text(
            "\"The structure of information,\nwhen properly exploited,\n"
            "transforms the seemingly impossible\ninto the trivially easy.\"",
            font_size=28,
            color=WHITE,
            line_spacing=1.5
        )
        
        self.play(Write(quote, run_time=3))
        self.wait(2)
        
        # End card
        self.play(FadeOut(quote), run_time=MEDIUM)
        
        end_title = Text("BINARY SEARCH", font_size=64, color=WHITE)
        end_title.set_color_by_gradient(BLUE, GREEN)
        
        end_subtitle = Text(
            "Think carefully about the structure of your problems.",
            font_size=24,
            color=GRAY
        )
        end_subtitle.next_to(end_title, DOWN, buff=0.8)
        
        self.play(Write(end_title), run_time=SLOW)
        self.play(FadeIn(end_subtitle, shift=UP * 0.3), run_time=MEDIUM)
        
        self.wait(3)
        
        # Fade to black
        self.play(
            FadeOut(end_title),
            FadeOut(end_subtitle),
            run_time=SLOW
        )


# =============================================================================
# MAIN COMBINED SCENE (for rendering complete video)
# =============================================================================

class BinarySearchComplete(Scene):
    """Complete video combining all scenes."""
    
    def construct(self):
        self.camera.background_color = BG_COLOR
        
        # Run all scenes in sequence
        # Note: In production, you might want to render scenes separately
        # and combine them, or use section markers for modularity
        
        scenes = [
            IntroductionScene,
            LinearSearchProblemScene,
            CoreInsightScene,
            AlgorithmInActionScene,
            MathematicsScene,
            CommonPitfallsScene,
            BeyondSearchingScene,
            ClosingScene,
        ]
        
        for scene_class in scenes:
            scene = scene_class()
            scene.construct()


# =============================================================================
# RENDER CONFIGURATION
# =============================================================================

if __name__ == "__main__":
    # To render individual scenes:
    # manim -pqh binary_search_visual.py IntroductionScene
    # 
    # To render complete video:
    # manim -pqh binary_search_visual.py BinarySearchComplete
    #
    # Quality flags:
    #   -ql : 480p 15fps (development)
    #   -qm : 720p 30fps (preview)
    #   -qh : 1080p 60fps (high quality)
    #   -qk : 4K 60fps (final render)
    #
    # For 1920x1080 @ 60fps:
    # manim -qh --fps 60 binary_search_visual.py IntroductionScene
    
    print("Binary Search Visualization - Manim Code")
    print("========================================")
    print("Render commands:")
    print("  Development: manim -pql binary_search_visual.py IntroductionScene")
    print("  High Quality: manim -pqh binary_search_visual.py BinarySearchComplete")
    print("  4K Final: manim -pqk binary_search_visual.py BinarySearchComplete")
