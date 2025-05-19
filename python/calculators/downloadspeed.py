from flask import jsonify
import re

def downloadspeed_solve(data):
    try:
        operation = data['operation']
        file_size_str = str(data.get('fileSize', '0'))
        size_pattern = re.compile(r'^([\d.]+)\s*(kb|mb|gb|tb)?', re.IGNORECASE)
        size_match = size_pattern.match(file_size_str.strip())
        if size_match:
            file_size_value = float(size_match.group(1))
            size_unit = size_match.group(2).lower() if size_match.group(2) else 'mb' 
        else:
            file_size_value = float(file_size_str)
            size_unit = 'mb'

        if size_unit == 'kb':
            file_size_mb = file_size_value / 1024
        elif size_unit == 'mb':
            file_size_mb = file_size_value
        elif size_unit == 'gb':
            file_size_mb = file_size_value * 1024
        elif size_unit == 'tb':
            file_size_mb = file_size_value * 1024 * 1024

        download_speed = float(data.get('downloadSpeed', 0))

        speed_unit = None
        if operation == 'mb/s':
            speed_unit = 'mb/s'            
        elif operation == 'mbps':
            speed_unit = 'mbps'
        else:
            return jsonify({'error': 'Failed to calculate...'})

    except (ValueError, TypeError) as e:
        print(f"Error parsing inputs: {e}")
        return jsonify({
            "error": "Invalid input: Please check file size and download speed formats"
        })

    if download_speed == 0:
        return jsonify({
            "error": "Download speed cannot be zero"
        })

    if speed_unit.lower() == 'mb/s':
        download_speed_mbs = download_speed
    elif speed_unit.lower() == 'mbps':
        download_speed_mbs = download_speed / 8
    else:
        return jsonify({
            "error": f"Invalid speed unit: {speed_unit}. Use 'mbps' or 'MB/s'."
        })

    total_seconds = file_size_mb / download_speed_mbs

    days = int(total_seconds // (24 * 3600))
    remaining_seconds = total_seconds % (24 * 3600)
    hours = int(remaining_seconds // 3600)
    remaining_seconds %= 3600
    minutes = int(remaining_seconds // 60)
    seconds = int(remaining_seconds % 60)

    time_parts = []
    if days > 0:
        time_parts.append(f"{days} day{'s' if days > 1 else ''}")
    if hours > 0 or days > 0:
        time_parts.append(f"{hours} hour{'s' if hours > 1 else ''}")
    if minutes > 0 or hours > 0 or days > 0:
        time_parts.append(f"{minutes} minute{'s' if minutes > 1 else ''}")
    if seconds > 0 or minutes > 0 or hours > 0 or days > 0:
        time_parts.append(f"{seconds} second{'s' if seconds > 1 else ''}")

    if len(time_parts) > 1:
        time_desc = ", ".join(time_parts[:-1]) + ", and " + time_parts[-1]
    else:
        time_desc = time_parts[0] if time_parts else "0 seconds"

    if total_seconds < 60:
        simple_time_desc = f"{total_seconds:.2f} seconds"
    elif total_seconds < 3600:
        simple_time_desc = f"{total_seconds/60:.2f} minutes"
    elif total_seconds < 86400:
        simple_time_desc = f"{total_seconds/3600:.2f} hours"
    elif total_seconds < 31536000:
        simple_time_desc = f"{total_seconds/86400:.2f} days"
    else:
        simple_time_desc = f"{total_seconds/31536000:.2f} years"

    print(f"time_desc: {time_desc}")
    print(f"simple_time_desc: {simple_time_desc}")

    if 'kb' in str(size_unit).lower():
        size_desc = f"{file_size_value} KB"
    elif 'mb' in str(size_unit).lower():
        size_desc = f"{file_size_value} MB"
    elif 'gb' in str(size_unit).lower():
        size_desc = f"{file_size_value} GB"
    elif 'tb' in str(size_unit).lower():
        size_desc = f"{file_size_value} TB"
    else:
        size_desc = f"{file_size_mb} MB"
    if speed_unit == 'mb/s':
        speed_unit = 'MB/s'
    return jsonify({
        'values': {
            'solution': f"It will take {time_desc} to download {size_desc} at {download_speed} {speed_unit}."
        }
    })