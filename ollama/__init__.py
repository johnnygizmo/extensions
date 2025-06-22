import bpy
import requests
import datetime


class OllamaAddonPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    model: bpy.props.StringProperty(
        name="Ollama Model",
        description="Name of the Ollama model to use",
        default="qwen2.5-coder"
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "model")

class TEXT_OT_send_to_ollama(bpy.types.Operator):
    bl_idname = "text.send_to_ollama"
    bl_label = "Send to Ollama"
    bl_description = (
        "Send selected text to Ollama and insert response into new text block"
    )
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        addon_prefs = context.preferences.addons[__name__].preferences
        model = addon_prefs.model
        space = context.space_data

        if space.type != "TEXT_EDITOR" or not space.text:
            self.report({"ERROR"}, "Not in a Text Editor or no text block open")
            return {"CANCELLED"}

        text_block = space.text

        # Get selection line/char positions
        start_line_idx = text_block.current_line_index
        end_line_idx = text_block.select_end_line_index
        start_char = text_block.current_character
        end_char = text_block.select_end_character

        # Sort selection direction
        if (start_line_idx > end_line_idx) or (
            start_line_idx == end_line_idx and start_char > end_char
        ):
            start_line_idx, end_line_idx = end_line_idx, start_line_idx
            start_char, end_char = end_char, start_char

        lines = text_block.lines
        selected_text = ""

        if start_line_idx == end_line_idx:
            # Single-line selection
            line = lines[start_line_idx].body
            selected_text = line[start_char:end_char]
        else:
            # Multi-line selection
            selected_lines = []
            for i in range(start_line_idx, end_line_idx + 1):
                line_text = lines[i].body
                if i == start_line_idx:
                    selected_lines.append(line_text[start_char:])
                elif i == end_line_idx:
                    selected_lines.append(line_text[:end_char])
                else:
                    selected_lines.append(line_text)
            selected_text = "\n".join(selected_lines)

        # Fallback if no selection
        if not selected_text.strip():
            selected_text = text_block.current_line.body

        print(selected_text)
        selected_text = (
            "The following is from a Blender 3d user: \n\n"
            + selected_text
        )

        # Send to Ollama
        try:
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={"model": model, "prompt": selected_text, "stream": False},
                timeout=10,
            )
            response.raise_for_status()
            result = response.json()
            output = result.get("response", "").strip()

            # Create a new text block
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            new_text = bpy.data.texts.new(name=f"Ollama_Response_{timestamp}")
            new_text.from_string(output)

            # Focus on the new text block
            space.text = new_text

            return {"FINISHED"}

        except Exception as e:
            self.report({"ERROR"}, f"Failed to contact Ollama: {e}")
            return {"CANCELLED"}


def menu_func(self, context):
    self.layout.operator("text.send_to_ollama", icon="CONSOLE")


def register():
    bpy.utils.register_class(OllamaAddonPreferences)
    bpy.utils.register_class(TEXT_OT_send_to_ollama)
    bpy.types.TEXT_MT_text.append(menu_func)

def unregister():
    bpy.types.TEXT_MT_text.remove(menu_func)
    bpy.utils.unregister_class(TEXT_OT_send_to_ollama)
    bpy.utils.unregister_class(OllamaAddonPreferences)


if __name__ == "__main__":
    register()
