# Image Zoom for Anki

Zoom the images on your cards during review without changing the size of the text.

| Action   | Shortcut (Cmd on macOS) |
|----------|-------------------------|
| Zoom in  | Ctrl+Shift+=            |
| Zoom out | Ctrl+Shift+-            |
| Reset    | Ctrl+Shift+0            |

Each press makes images 25% larger or smaller, from 50% up to 1000% (about eleven presses to reach the top). A tooltip shows the current level, and Anki remembers it per profile. You can change the shortcuts and limits in Tools > Add-ons > Image Zoom > Config.

Anki's own View > Zoom (Ctrl+= / Ctrl+-) still zooms the whole page. This add-on scales only images. Image occlusion cards and whiteboard drawings are left as they are.

## Development

- Symlink `src/` into your add-ons folder as `image_zoom` (Tools > Add-ons > View Files shows where that folder is), then restart Anki.
- `./build.sh` creates `image_zoom.ankiaddon` for upload to https://ankiweb.net/shared/addons.

## License

MIT. See [LICENSE](LICENSE).
