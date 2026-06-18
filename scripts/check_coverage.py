import sys
import xml.etree.ElementTree as ET


def main() -> int:
    target = 90.0
    coverage_file = "coverage.xml"

    try:
        tree = ET.parse(coverage_file)
        root = tree.getroot()
        line_rate = float(root.attrib.get("line-rate", "0"))
        percent = line_rate * 100
    except Exception as exc:
        print(f"❌ Failed to read coverage.xml: {exc}")
        return 1

    print(f"Coverage: {percent:.2f}%")
    print(f"Target: {target:.2f}%")

    if percent < target:
        print("❌ Coverage gate failed.")
        return 1

    print("✅ Coverage gate passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
