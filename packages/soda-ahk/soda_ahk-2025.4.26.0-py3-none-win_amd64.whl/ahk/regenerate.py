from pathlib import Path
import sys
import winreg
import logging


home_folder = Path.home()
python_path = Path(sys.executable).resolve().parent
start_folder = home_folder.joinpath(
    r"AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup"
)


CURRENT = Path(__file__).resolve().parent
scripts = CURRENT.parent.joinpath("ahk_scripts")

logging.basicConfig(
    filename=CURRENT.parent.joinpath("soda-ahk.reg.log"), level=logging.INFO
)

logger = logging.getLogger(__name__)


def resolve_ahk_chm():
    script_type = ""
    script_exec = ""
    try:
        with winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, ".ahk") as key:
            script_type = winreg.QueryValue(key, "")
    except OSError:
        logger.error(".ahk ext not found in registry")
    try:
        # \AutoHotkeyScript\Shell\Open\Command
        with winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, script_type) as key:
            script_exec = winreg.QueryValue(key, r"Shell\Open\Command")
    except OSError:
        logger.error("query exec failed")
    logger.info("current exec: %s", script_exec)

    if script_exec != "":
        ahk_exe = script_exec.split(" ")[0]
        # need to remove start " and end "
        ahk_exe = ahk_exe[1:-1]
        chm = (
            Path(ahk_exe)
            .resolve()
            .parent.parent.joinpath("v2")
            .joinpath("AutoHotkey.chm")
        )
        if chm.exists():
            return chm

    logger.error("error reading reg, using default path")
    return home_folder.joinpath(r"scoop\apps\autohotkey\current\v2\AutoHotkey.chm")


vars = {
    "resources": CURRENT.parent.joinpath("ahk_resources"),
    "cursor": CURRENT.parent.joinpath("ahk_cursor"),
    "{AutoHotkey.chm}": resolve_ahk_chm(),
    "desktop": home_folder.joinpath("Desktop"),
}


def regenerate():
    templates = CURRENT.parent.joinpath("ahk_script_templates")
    scripts.mkdir(exist_ok=True)
    files = list(templates.glob("*.ahk"))
    for f in files:
        content = f.read_text(encoding="utf8")
        for k, v in vars.items():
            if "{" not in k:
                k = "{" + k + "}"
            content = content.replace(k, str(v))
        dest_file = scripts.joinpath(f.stem.removesuffix(".template") + ".ahk")
        dest_file.write_text(content, encoding="utf8")


if __name__ == "__main__":
    regenerate()
