import os
import uuid
import cv2
import numpy as np

class SkinAnalyzer:
    def __init__(self):
        pass

    def process_image(self, input_path: str, output_dir: str) -> dict:
        """
        Analyze a Dermatology / Skin Lesion image for asymmetry, border irregularity, and pigmentation.
        """
        filename = os.path.basename(input_path)
        base_name, _ = os.path.splitext(filename)
        
        img = cv2.imread(input_path)
        if img is None:
            raise ValueError(f"Failed to load skin image: {input_path}")
            
        h, w = img.shape[:2]
        img_grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Apply Gaussian Blur and Otsu thresholding for lesion segmentation
        blurred = cv2.GaussianBlur(img_grey, (7, 7), 0)
        
        # Skin lesions are usually darker than background skin
        _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        
        # Morphological cleanup
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        cleaned = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)
        cleaned = cv2.morphologyEx(cleaned, cv2.MORPH_OPEN, kernel, iterations=1)
        
        # Find contours and keep largest central contour as primary lesion
        contours, _ = cv2.findContours(cleaned, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        mask = np.zeros_like(img_grey)
        detected = False
        lesion_area_pct = 0.0
        findings_list = []
        
        if contours:
            # Sort by area descending
            contours = sorted(contours, key=cv2.contourArea, reverse=True)
            largest = contours[0]
            area = cv2.contourArea(largest)
            total_area = h * w
            
            if area > (total_area * 0.02): # at least 2% of image frame
                cv2.drawContours(mask, [largest], -1, 255, -1)
                detected = True
                lesion_area_pct = (area / total_area) * 100
                
                # Asymmetry Check: Compare left vs right half of bounding box
                x, y, bw, bh = cv2.boundingRect(largest)
                lesion_crop = mask[y:y+bh, x:x+bw]
                half_w = bw // 2
                left_half = lesion_crop[:, :half_w]
                right_half = cv2.flip(lesion_crop[:, half_w:half_w*2], 1)
                
                min_h = min(left_half.shape[0], right_half.shape[0])
                min_w = min(left_half.shape[1], right_half.shape[1])
                diff = np.abs(left_half[:min_h, :min_w] - right_half[:min_h, :min_w])
                asymmetry_ratio = np.count_nonzero(diff) / max(1, area)
                
                if asymmetry_ratio > 0.25:
                    findings_list.append("Significant structural asymmetry detected")
                else:
                    findings_list.append("Symmetrical lesion boundary")
                    
                # Border Irregularity Check
                perimeter = cv2.arcLength(largest, True)
                compactness = (4 * np.pi * area) / (perimeter ** 2 + 1e-5)
                if compactness < 0.6:
                    findings_list.append("Irregular/notched lesion borders")
                else:
                    findings_list.append("Regular border perimeter")
                    
                # Color Variation Check
                lesion_rgb = img[y:y+bh, x:x+bw]
                mask_crop = mask[y:y+bh, x:x+bw]
                lesion_pixels = lesion_rgb[mask_crop > 0]
                if len(lesion_pixels) > 0:
                    std_dev = np.std(lesion_pixels, axis=0)
                    mean_std = np.mean(std_dev)
                    if mean_std > 35:
                        findings_list.append("Multi-chromatic pigmentation / variegated color distribution")
                    else:
                        findings_list.append("Uniform pigmentation distribution")
                        
        if not detected:
            findings_text = "Dermatological scan clear. No suspicious pigmentary or structural lesions detected."
            confidence_str = "0.00%"
        else:
            findings_text = f"Dermatology scan complete. Primary skin lesion area: {lesion_area_pct:.1f}% frame coverage. " + " | ".join(findings_list)
            confidence_str = f"{lesion_area_pct:.2f}%"
            
        # Create AI Overlay (Red translucent fill + Orange contour outline)
        overlay = img.copy()
        red_mask = np.zeros_like(img)
        red_mask[mask > 0] = [0, 0, 220] # Red
        
        cv2.addWeighted(red_mask, 0.45, overlay, 0.55, 0, overlay)
        
        # Orange outline
        contours_to_draw, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(overlay, contours_to_draw, -1, (0, 140, 255), 2)
        
        # Save mask and overlay outputs
        uid = uuid.uuid4().hex[:8]
        mask_filename = f"{uid}_{base_name}_mask.png"
        overlay_filename = f"{uid}_{base_name}_overlay.png"
        
        cv2.imwrite(os.path.join(output_dir, mask_filename), mask)
        cv2.imwrite(os.path.join(output_dir, overlay_filename), overlay)
        
        return {
            'modality': 'DERMATO',
            'detected': detected,
            'confidence': confidence_str,
            'mask_filename': mask_filename,
            'overlay_filename': overlay_filename,
            'findings_text': findings_text
        }

_analyzer = None

def get_skin_analyzer() -> SkinAnalyzer:
    global _analyzer
    if _analyzer is None:
        _analyzer = SkinAnalyzer()
    return _analyzer
