"""
Gradio Interface for Taj Chat

Beautiful UI for video creation.
"""

import asyncio
import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

# Import gradio only when needed
try:
    import gradio as gr
    GRADIO_AVAILABLE = True
except ImportError:
    GRADIO_AVAILABLE = False
    logger.warning("Gradio not installed. Install with: pip install gradio")


def create_interface(workflow_engine=None):
    """Create Gradio interface for Taj Chat."""

    if not GRADIO_AVAILABLE:
        logger.error("Gradio not available")
        return None

    async def generate_video(
        prompt: str,
        mode: str,
        platforms: list[str],
        progress=gr.Progress(),
    ):
        """Generate video with progress tracking."""

        if not workflow_engine:
            return "Error: Workflow engine not initialized", None

        progress(0, desc="Starting video generation...")

        from ..workflows.engine import WorkflowMode

        mode_map = {
            "Sequential (Best Quality)": WorkflowMode.SEQUENTIAL,
            "Parallel (Fastest)": WorkflowMode.PARALLEL,
            "Hybrid (Balanced)": WorkflowMode.HYBRID,
        }
        workflow_mode = mode_map.get(mode, WorkflowMode.HYBRID)

        # Map platform display names
        platform_map = {
            "TikTok": "tiktok",
            "Instagram Reels": "instagram_reels",
            "YouTube Shorts": "youtube_shorts",
            "Twitter/X": "twitter",
        }
        target_platforms = [platform_map.get(p, p.lower()) for p in platforms]

        progress(0.1, desc="Analyzing content...")

        try:
            result = await workflow_engine.create_video(
                prompt=prompt,
                mode=workflow_mode,
                platforms=target_platforms,
            )

            progress(1.0, desc="Complete!")

            # Format output
            status_text = f"""
## Video Generation Complete!

**Workflow ID:** {result.workflow_id}
**Status:** {result.status}
**Mode:** {result.mode.value}
**Execution Time:** {result.total_execution_time_ms:.0f}ms

### Output Files:
{chr(10).join(f'- {f}' for f in result.output_files) if result.output_files else 'No files generated'}

### Agent Results:
{chr(10).join(f'- {k}: {v.status}' for k, v in result.agent_results.items())}

### Errors:
{chr(10).join(f'- {e}' for e in result.errors) if result.errors else 'None'}
"""

            # Return first video file if available
            video_file = None
            if result.output_files:
                for f in result.output_files:
                    if str(f).endswith('.mp4'):
                        video_file = str(f)
                        break

            return status_text, video_file

        except Exception as e:
            logger.error(f"Generation error: {e}")
            return f"Error: {str(e)}", None

    def sync_generate(prompt, mode, platforms, progress=gr.Progress()):
        """Synchronous wrapper for async generation."""
        return asyncio.run(generate_video(prompt, mode, platforms, progress))

    # Create Gradio interface
    with gr.Blocks(
        title="Taj Chat - AI Video Creator",
        theme=gr.themes.Soft(
            primary_hue="purple",
            secondary_hue="blue",
        ),
        css="""
        .gradio-container {
            max-width: 1200px !important;
        }
        .header {
            text-align: center;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 10px;
            margin-bottom: 20px;
        }
        .header h1 {
            color: white;
            margin: 0;
        }
        """,
    ) as interface:

        # Header
        gr.HTML("""
        <div class="header">
            <h1>🎬 Taj Chat</h1>
            <p style="color: white; opacity: 0.9;">Ultimate AI Video Creation Platform</p>
            <p style="color: white; opacity: 0.7; font-size: 0.9em;">10x Specialist AI Agents • Sequential & Parallel Workflows</p>
        </div>
        """)

        with gr.Row():
            with gr.Column(scale=2):
                # Input section
                prompt_input = gr.Textbox(
                    label="Video Description",
                    placeholder="Describe the video you want to create...\n\nExample: Create an energetic video about the benefits of morning exercise with upbeat music and motivational text overlays",
                    lines=4,
                )

                with gr.Row():
                    mode_select = gr.Dropdown(
                        choices=[
                            "Hybrid (Balanced)",
                            "Sequential (Best Quality)",
                            "Parallel (Fastest)",
                        ],
                        value="Hybrid (Balanced)",
                        label="Workflow Mode",
                    )

                    platform_select = gr.CheckboxGroup(
                        choices=["TikTok", "Instagram Reels", "YouTube Shorts", "Twitter/X"],
                        value=["TikTok"],
                        label="Target Platforms",
                    )

                generate_btn = gr.Button(
                    "🎬 Generate Video",
                    variant="primary",
                    size="lg",
                )

            with gr.Column(scale=1):
                # Info panel
                gr.Markdown("""
                ### 🤖 10x AI Agents

                1. **Content Analysis** - Script & SEO
                2. **Video Generation** - AI video creation
                3. **Music Generation** - Custom soundtrack
                4. **Image Generation** - Overlays & thumbnails
                5. **Voice & Speech** - Narration & captions
                6. **Editing** - Composition & effects
                7. **Optimization** - Platform encoding
                8. **Analytics** - Performance prediction
                9. **Safety** - Content moderation
                10. **Social Media** - Upload & scheduling

                ### 🔧 Workflow Modes

                - **Sequential**: Best quality, step-by-step
                - **Parallel**: Fastest, concurrent generation
                - **Hybrid**: Balanced approach
                """)

        # Output section
        with gr.Row():
            with gr.Column():
                output_text = gr.Markdown(label="Generation Status")
            with gr.Column():
                output_video = gr.Video(label="Generated Video")

        # Connect button to function
        generate_btn.click(
            fn=sync_generate,
            inputs=[prompt_input, mode_select, platform_select],
            outputs=[output_text, output_video],
        )

        # Examples
        gr.Examples(
            examples=[
                ["Create a 30-second motivational video about achieving your goals with epic music and inspiring text overlays"],
                ["Make a fun cooking tutorial showing how to make a quick breakfast smoothie"],
                ["Generate a travel video showcasing beautiful sunset views with relaxing ambient music"],
                ["Create an educational video explaining how AI works in simple terms"],
            ],
            inputs=prompt_input,
        )

    return interface


def launch_ui(workflow_engine=None, share: bool = False, port: int = 7860):
    """Launch the Gradio UI."""

    interface = create_interface(workflow_engine)

    if interface:
        interface.launch(
            share=share,
            server_port=port,
            server_name="0.0.0.0",
        )
    else:
        logger.error("Failed to create interface")
