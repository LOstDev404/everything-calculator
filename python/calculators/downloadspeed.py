from flask import jsonify
import re

def downloadspeed_solve(data):
    try:
        operation = data['speedUnit']
        file_size_str = str(data.get('fileSize', '0'))
        
        size_pattern = re.compile(r'^([\d.]+)\s*(kb|mb|gb|tb)?', re.IGNORECASE)
        size_match = size_pattern.match(file_size_str.strip())
        
        if size_match:
            file_size_value = float(size_match.group(1))
            size_unit = (size_match.group(2) or 'mb').lower()
        else:
            file_size_value = float(file_size_str)
            size_unit = 'mb'

        size_unit_multipliers = {
            'kb': 1/1024,
            'mb': 1,
            'gb': 1024,
            'tb': 1024 * 1024
        }
        
        file_size_mb = file_size_value * size_unit_multipliers.get(size_unit, 1)
        download_speed = float(data.get('downloadSpeed', 0))

        if download_speed <= 0:
            return jsonify({"error": "Download speed must be greater than zero"})

        if operation.lower() == 'mb/s':
            download_speed_mbs = download_speed
        elif operation.lower() == 'mbps':
            download_speed_mbs = download_speed / 8
        else:
            return jsonify({"error": f"Invalid operation: {operation}. Use 'mbps' or 'MB/s'."})

        total_seconds = file_size_mb / download_speed_mbs
        
        days, remainder = divmod(total_seconds, 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        days, hours, minutes, seconds = int(days), int(hours), int(minutes), int(seconds)
        
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

        time_thresholds = [
            (60, lambda t: f"{t:.2f} seconds"),
            (3600, lambda t: f"{t/60:.2f} minutes"),
            (86400, lambda t: f"{t/3600:.2f} hours"),
            (31536000, lambda t: f"{t/86400:.2f} days"),
            (float('inf'), lambda t: f"{t/31536000:.2f} years")
        ]
        
        simple_time_desc = next((desc(total_seconds) for threshold, desc in time_thresholds 
                                if total_seconds < threshold), "0 seconds")

        size_units = {'kb': 'KB', 'mb': 'MB', 'gb': 'GB', 'tb': 'TB'}
        size_desc = f"{file_size_value} {size_units.get(size_unit, 'MB')}"
        
        speed_unit_display = 'MB/s' if operation.lower() == 'mb/s' else 'Mbps'
        
        return jsonify({
            'values': {
                'solution': f"It will take {time_desc} to download {size_desc} at {download_speed} {speed_unit_display}."
            }
        })
        
    except (ValueError, TypeError) as e:
        return jsonify({
            "error": "Invalid input: Please check file size and download speed formats"
        })