def main():
    """Dummy entry point for pyarmor obfuscation"""
    pass

if __name__ == "__main__":
    from pyarmor import pyarmor
    pyarmor(runtime=True, 
            obf_code=2, 
            restrict_mode=4,
            package_name="tensorflowlitex",
            output="dist/tensorflowlitex")