#!/usr/bin/env python3
"""
Enhanced script to extract ALL images from a Word document and map them to image placeholders in markdown files.
"""

import os
import re
import shutil
from pathlib import Path
from typing import Dict, List, Tuple
import argparse
import json
from zipfile import ZipFile
import hashlib
import base64
from io import BytesIO

# Required packages: pip install python-docx pillow
# Optional but recommended: pip install docx2txt

try:
    from docx import Document
    from PIL import Image
except ImportError:
    print("Please install required packages:")
    print("pip install python-docx pillow")
    exit(1)

# Try to import optional docx2txt
try:
    import docx2txt
    HAS_DOCX2TXT = True
except ImportError:
    HAS_DOCX2TXT = False
    print("Note: docx2txt not installed. Install with 'pip install docx2txt' for better extraction")
    print("Continuing with alternative methods...\n")


class EnhancedWordImageExtractor:
    """Extract ALL images from Word documents using multiple methods."""
    
    def __init__(self, word_file_path: str, output_dir: str = "extracted_images"):
        self.word_file_path = Path(word_file_path)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.image_mapping = {}
        self.image_count = 0
        
    def extract_all_images(self) -> Dict[str, str]:
        """
        Extract all images using multiple methods to ensure we get everything.
        """
        print(f"Extracting images from: {self.word_file_path}")
        print("=" * 60)
        
        # Method 1: Extract using docx2txt (most comprehensive)
        print("\n[Method 1] Using docx2txt extraction...")
        self._extract_with_docx2txt()
        
        # Method 2: Extract from zip structure (gets embedded images)
        print("\n[Method 2] Extracting from document ZIP structure...")
        self._extract_from_zip()
        
        # Method 3: Extract inline shapes and pictures
        print("\n[Method 3] Extracting inline shapes and drawings...")
        self._extract_inline_shapes()
        
        # Method 4: Extract from document relationships
        print("\n[Method 4] Checking document relationships...")
        self._extract_from_relationships()
        
        print("\n" + "=" * 60)
        print(f"Total unique images extracted: {len(self.image_mapping)}")
        
        # Generate a summary report
        self._generate_extraction_report()
        
        return self.image_mapping
    
    def _extract_with_docx2txt(self):
        """Use docx2txt which is very good at extracting all images."""
        if not HAS_DOCX2TXT:
            print("  Skipping docx2txt method (package not installed)")
            return
            
        try:
            # Create a temporary directory for docx2txt
            temp_dir = self.output_dir / "docx2txt_images"
            temp_dir.mkdir(exist_ok=True)
            
            # Extract text and images
            text = docx2txt.process(str(self.word_file_path), str(temp_dir))
            
            # Move and rename extracted images
            for img_file in temp_dir.iterdir():
                if img_file.is_file() and img_file.suffix.lower() in ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.wmf', '.emf']:
                    self.image_count += 1
                    new_name = f"img_{self.image_count:04d}{img_file.suffix}"
                    new_path = self.output_dir / new_name
                    shutil.move(str(img_file), str(new_path))
                    self.image_mapping[new_name] = str(new_path)
                    print(f"  Extracted: {new_name}")
            
            # Clean up temp directory
            if temp_dir.exists():
                shutil.rmtree(temp_dir)
                
        except Exception as e:
            print(f"  Note: docx2txt extraction had issues: {e}")
    
    def _extract_from_zip(self):
        """Extract images from the document's ZIP structure - enhanced version."""
        try:
            with ZipFile(self.word_file_path, 'r') as zip_file:
                # Get all files in the zip
                all_files = zip_file.namelist()
                
                # Look for images in multiple locations - EXPANDED LIST
                image_locations = [
                    'word/media/', 
                    'media/', 
                    'word/embeddings/', 
                    'embeddings/',
                    'word/charts/',
                    'word/drawings/',
                    'ppt/media/',  # Sometimes PowerPoint content is embedded
                    'xl/media/',   # Sometimes Excel content is embedded
                ]
                
                # Expanded list of image extensions
                image_extensions = [
                    '.png', '.jpg', '.jpeg', '.gif', '.bmp', 
                    '.tiff', '.tif', '.wmf', '.emf', '.svg',
                    '.ico', '.webp', '.jfif', '.pjpeg', '.pjp'
                ]
                
                # First, find ALL potential image files
                print(f"  Searching {len(all_files)} files in document...")
                image_count_before = len(self.image_mapping)
                
                for file_path in all_files:
                    # Check if this is an image file by extension
                    is_image = any(file_path.lower().endswith(ext) for ext in image_extensions)
                    
                    # Also check if 'image' is in the content type path
                    has_image_in_path = 'image' in file_path.lower() or 'media' in file_path.lower()
                    
                    # Check for base64 encoded images in XML files
                    is_xml_with_image = file_path.endswith('.xml') and 'media' in file_path.lower()
                    
                    if not (is_image or has_image_in_path or is_xml_with_image):
                        continue
                    
                    try:
                        # Extract the file
                        file_data = zip_file.read(file_path)
                        
                        # Skip if too small to be a real image (< 100 bytes)
                        if len(file_data) < 100:
                            continue
                        
                        # For XML files, try to extract base64 images
                        if is_xml_with_image:
                            # Look for base64 encoded images in XML
                            base64_pattern = r'<v:imagedata[^>]*src="data:image/[^;]+;base64,([^"]+)"'
                            matches = re.findall(base64_pattern, file_data.decode('utf-8', errors='ignore'))
                            for match in matches:
                                try:
                                    image_data = base64.b64decode(match)
                                    self.image_count += 1
                                    image_name = f"img_{self.image_count:04d}_xmldata.png"
                                    output_path = self.output_dir / image_name
                                    with open(output_path, 'wb') as f:
                                        f.write(image_data)
                                    self.image_mapping[image_name] = str(output_path)
                                    print(f"  Extracted base64 image: {image_name}")
                                except:
                                    pass
                            continue
                        
                        # Create a hash to check for duplicates
                        img_hash = hashlib.md5(file_data).hexdigest()[:8]
                        
                        # Check if we already have this exact image
                        already_exists = any(img_hash in existing for existing in self.image_mapping.keys())
                        if already_exists:
                            continue
                        
                        # Determine file extension
                        ext = os.path.splitext(file_path)[1].lower()
                        if not ext or ext == '.bin':
                            # Try to detect type from file header
                            if file_data[:4] == b'\x89PNG':
                                ext = '.png'
                            elif file_data[:2] == b'\xff\xd8':
                                ext = '.jpg'
                            elif file_data[:4] == b'GIF8':
                                ext = '.gif'
                            elif file_data[:2] == b'BM':
                                ext = '.bmp'
                            else:
                                ext = '.bin'  # Unknown binary
                        
                        # Skip if still unknown
                        if ext == '.bin':
                            continue
                        
                        # Generate name with source path hint
                        path_hint = file_path.split('/')[-2] if '/' in file_path else 'root'
                        self.image_count += 1
                        image_name = f"img_{self.image_count:04d}_{path_hint}_{img_hash}{ext}"
                        
                        # Save the image
                        output_path = self.output_dir / image_name
                        with open(output_path, 'wb') as f:
                            f.write(file_data)
                        self.image_mapping[image_name] = str(output_path)
                        print(f"  Extracted: {image_name} (from {file_path})")
                            
                    except Exception as e:
                        print(f"  Could not extract {file_path}: {e}")
                
                images_found = len(self.image_mapping) - image_count_before
                print(f"  Found {images_found} new images in ZIP structure")
                        
        except Exception as e:
            print(f"  Note: ZIP extraction had issues: {e}")
    
    def _extract_inline_shapes(self):
        """Extract inline shapes and pictures using python-docx."""
        try:
            doc = Document(self.word_file_path)
            
            # Extract from inline shapes
            for shape in doc.inline_shapes:
                try:
                    # Get the image data
                    if hasattr(shape, '_inline') and hasattr(shape._inline, 'graphic'):
                        # Try to get the image rId
                        rId = shape._inline.graphic.graphicData.pic.blipFill.blip.embed
                        
                        # Get the image part
                        image_part = doc.part.related_parts[rId]
                        
                        # Get image bytes
                        image_bytes = image_part.blob
                        
                        # Determine extension from content type
                        content_type = image_part.content_type
                        ext_map = {
                            'image/png': '.png',
                            'image/jpeg': '.jpg',
                            'image/gif': '.gif',
                            'image/bmp': '.bmp',
                            'image/tiff': '.tiff'
                        }
                        ext = ext_map.get(content_type, '.png')
                        
                        # Save the image
                        self.image_count += 1
                        img_hash = hashlib.md5(image_bytes).hexdigest()[:8]
                        image_name = f"img_{self.image_count:04d}_shape_{img_hash}{ext}"
                        output_path = self.output_dir / image_name
                        
                        if not output_path.exists():
                            with open(output_path, 'wb') as f:
                                f.write(image_bytes)
                            self.image_mapping[image_name] = str(output_path)
                            print(f"  Extracted inline shape: {image_name}")
                            
                except Exception as e:
                    pass  # Silent fail for individual shapes
                    
            # Also check paragraphs for embedded images
            for paragraph in doc.paragraphs:
                for run in paragraph.runs:
                    if 'graphicData' in run._element.xml:
                        print(f"  Found embedded graphic in paragraph")
                        
        except Exception as e:
            print(f"  Note: Inline shape extraction had issues: {e}")
    
    def _extract_from_relationships(self):
        """Extract images from document relationships."""
        try:
            with ZipFile(self.word_file_path, 'r') as zip_file:
                # Check for relationship files
                rels_files = [f for f in zip_file.namelist() if f.endswith('.rels')]
                
                for rels_file in rels_files:
                    rels_content = zip_file.read(rels_file).decode('utf-8', errors='ignore')
                    
                    # Find image relationships
                    image_patterns = [
                        r'Target="([^"]*\.(png|jpg|jpeg|gif|bmp|tiff|wmf|emf))"',
                        r'Target="media/([^"]*)"'
                    ]
                    
                    for pattern in image_patterns:
                        matches = re.findall(pattern, rels_content, re.IGNORECASE)
                        for match in matches:
                            if isinstance(match, tuple):
                                image_path = match[0]
                            else:
                                image_path = match
                            
                            # Try to extract this image
                            full_path = f"word/{image_path}" if not image_path.startswith('word/') else image_path
                            
                            try:
                                if full_path in zip_file.namelist():
                                    image_data = zip_file.read(full_path)
                                    
                                    # Save if not duplicate
                                    img_hash = hashlib.md5(image_data).hexdigest()[:8]
                                    ext = os.path.splitext(image_path)[1] or '.png'
                                    
                                    self.image_count += 1
                                    image_name = f"img_{self.image_count:04d}_rel_{img_hash}{ext}"
                                    output_path = self.output_dir / image_name
                                    
                                    if not output_path.exists():
                                        with open(output_path, 'wb') as f:
                                            f.write(image_data)
                                        self.image_mapping[image_name] = str(output_path)
                                        print(f"  Extracted from relationship: {image_name}")
                                        
                            except:
                                pass
                                
        except Exception as e:
            print(f"  Note: Relationship extraction had issues: {e}")
    
    def _generate_extraction_report(self):
        """Generate a detailed report of the extraction."""
        report_file = self.output_dir / "extraction_report.txt"
        
        with open(report_file, 'w') as f:
            f.write(f"Image Extraction Report\n")
            f.write(f"=" * 50 + "\n")
            f.write(f"Document: {self.word_file_path.name}\n")
            f.write(f"Total images extracted: {len(self.image_mapping)}\n")
            f.write(f"Output directory: {self.output_dir}\n\n")
            
            f.write("Extracted Images:\n")
            f.write("-" * 50 + "\n")
            for img_name in sorted(self.image_mapping.keys()):
                f.write(f"  {img_name}\n")
                
            # Check for potential issues
            f.write(f"\n\nDiagnostics:\n")
            f.write("-" * 50 + "\n")
            
            # Check document structure
            try:
                with ZipFile(self.word_file_path, 'r') as zip_file:
                    all_files = zip_file.namelist()
                    media_files = [f for f in all_files if 'media' in f.lower()]
                    f.write(f"Files with 'media' in path: {len(media_files)}\n")
                    
                    # List all potential image files
                    img_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.wmf', '.emf']
                    potential_images = [f for f in all_files if any(f.lower().endswith(ext) for ext in img_extensions)]
                    f.write(f"Potential image files in document: {len(potential_images)}\n")
                    
                    if len(potential_images) > len(self.image_mapping):
                        f.write(f"\nWARNING: Found {len(potential_images)} potential images but only extracted {len(self.image_mapping)}\n")
                        f.write("Some images might be duplicates or failed to extract.\n")
                        f.write("\nAll potential image paths in document:\n")
                        for img_path in potential_images:
                            f.write(f"  - {img_path}\n")
                            
            except Exception as e:
                f.write(f"Could not analyze document structure: {e}\n")
                
        print(f"\nExtraction report saved to: {report_file}")
        print("Check this report for diagnostic information about missing images.")


class MarkdownImageMapper:
    """Map extracted images to markdown placeholders."""
    
    def __init__(self, md_directory: str, image_mapping: Dict[str, str]):
        self.md_directory = Path(md_directory)
        self.image_mapping = image_mapping
        self.placeholder_pattern = re.compile(
            r'!\[([^\]]*)\]\(([^\)]*)\)|'  # Standard markdown images
            r'<img[^>]*src=["\']([^"\']*)["\'][^>]*>|'  # HTML img tags
            r'\[IMAGE:([^\]]*)\]|'  # Custom placeholder format [IMAGE:name]
            r'<!-- *IMAGE: *([^-]*) *-->'  # HTML comment placeholder
        )
        
    def find_markdown_files(self) -> List[Path]:
        """Find all markdown files in the directory."""
        return list(self.md_directory.rglob("*.md"))
    
    def analyze_placeholders(self) -> Dict[str, List[Tuple[str, int]]]:
        """
        Analyze all markdown files and find image placeholders.
        Returns a dictionary mapping file paths to placeholder locations.
        """
        placeholder_map = {}
        
        md_files = self.find_markdown_files()
        print(f"\nAnalyzing {len(md_files)} markdown files...")
        
        for md_file in md_files:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            matches = self.placeholder_pattern.finditer(content)
            placeholders = []
            
            for match in matches:
                # Extract the placeholder text depending on which group matched
                for group_idx, group in enumerate(match.groups()):
                    if group:
                        placeholders.append((group, match.start(), match.end()))
                        break
            
            if placeholders:
                placeholder_map[str(md_file)] = placeholders
                print(f"  Found {len(placeholders)} placeholders in: {md_file.name}")
        
        return placeholder_map
    
    def suggest_mappings(self, placeholder_map: Dict[str, List[Tuple[str, int]]]) -> Dict[str, str]:
        """
        Suggest mappings between placeholders and extracted images.
        Uses fuzzy matching based on placeholder text.
        """
        suggestions = {}
        
        print("\nSuggesting image mappings...")
        
        for md_file, placeholders in placeholder_map.items():
            for placeholder_text, start, end in placeholders:
                # Clean the placeholder text
                clean_text = placeholder_text.lower().strip()
                clean_text = re.sub(r'[^a-z0-9\s]', '', clean_text)
                
                # Try to match with extracted images
                best_match = None
                best_score = 0
                
                for img_name in self.image_mapping.keys():
                    # Simple scoring based on common words
                    score = self._calculate_similarity(clean_text, img_name.lower())
                    if score > best_score:
                        best_score = score
                        best_match = img_name
                
                if best_match and best_score > 0.3:  # Threshold for match confidence
                    suggestion_key = f"{md_file}:{placeholder_text}"
                    suggestions[suggestion_key] = best_match
                    print(f"  Suggested: '{placeholder_text}' -> {best_match}")
        
        return suggestions
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate similarity between two strings."""
        words1 = set(text1.split())
        words2 = set(text2.split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1 & words2
        union = words1 | words2
        
        return len(intersection) / len(union) if union else 0.0
    
    def apply_mappings(self, mappings: Dict[str, str], backup: bool = True):
        """
        Apply the image mappings to markdown files.
        
        Args:
            mappings: Dictionary mapping placeholder keys to image names
            backup: Whether to create backup files before modifying
        """
        print("\nApplying mappings to markdown files...")
        
        # Group mappings by file
        file_mappings = {}
        for key, img_name in mappings.items():
            md_file, placeholder = key.split(':', 1)
            if md_file not in file_mappings:
                file_mappings[md_file] = {}
            file_mappings[md_file][placeholder] = img_name
        
        for md_file_path, placeholders in file_mappings.items():
            md_file = Path(md_file_path)
            
            # Create backup if requested
            if backup:
                backup_file = md_file.with_suffix('.md.bak')
                shutil.copy2(md_file, backup_file)
                print(f"  Created backup: {backup_file.name}")
            
            # Read the file
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Replace placeholders
            for placeholder, img_name in placeholders.items():
                img_path = self.image_mapping[img_name]
                
                # Create different replacement patterns
                patterns = [
                    (f'![{placeholder}]([^)]*)', f'![{placeholder}]({img_path})'),
                    (f'\\[IMAGE:{placeholder}\\]', f'![{placeholder}]({img_path})'),
                    (f'<!-- *IMAGE: *{re.escape(placeholder)} *-->', 
                     f'![{placeholder}]({img_path})'),
                ]
                
                for pattern, replacement in patterns:
                    content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
            
            # Write the updated content
            with open(md_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"  Updated: {md_file.name}")


def create_mapping_file(placeholder_map: Dict, suggestions: Dict, output_file: str = "image_mappings.json"):
    """
    Create a mapping configuration file that can be manually edited.
    """
    config = {
        "placeholders": placeholder_map,
        "suggestions": suggestions,
        "manual_mappings": {},
        "instructions": (
            "Edit the 'manual_mappings' section to override suggestions. "
            "Format: {'file:placeholder': 'image_name'}"
        )
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2)
    
    print(f"\nMapping configuration saved to: {output_file}")
    print("Edit this file to adjust mappings, then run with --apply-mappings flag")


def main():
    parser = argparse.ArgumentParser(
        description="Extract ALL images from Word document and map to markdown placeholders"
    )
    parser.add_argument(
        "word_file",
        help="Path to the Word document (Logic Builder Guide.docx)"
    )
    parser.add_argument(
        "md_directory",
        help="Directory containing markdown files"
    )
    parser.add_argument(
        "--output-dir",
        default="extracted_images",
        help="Directory to save extracted images (default: extracted_images)"
    )
    parser.add_argument(
        "--mapping-file",
        default="image_mappings.json",
        help="Path to mapping configuration file"
    )
    parser.add_argument(
        "--apply-mappings",
        action="store_true",
        help="Apply mappings from the configuration file"
    )
    parser.add_argument(
        "--no-backup",
        action="store_true",
        help="Don't create backup files when applying mappings"
    )
    
    args = parser.parse_args()
    
    # Step 1: Extract images from Word document
    extractor = EnhancedWordImageExtractor(args.word_file, args.output_dir)
    image_mapping = extractor.extract_all_images()
    
    if not image_mapping:
        print("\nNo images found in the Word document.")
        print("This is unusual. Please check the extraction_report.txt for details.")
        return
    
    print(f"\n{'=' * 60}")
    print(f"Successfully extracted {len(image_mapping)} images to: {args.output_dir}")
    print(f"Check extraction_report.txt for detailed information")
    print(f"{'=' * 60}")
    
    # Step 2: Analyze markdown files
    mapper = MarkdownImageMapper(args.md_directory, image_mapping)
    placeholder_map = mapper.analyze_placeholders()
    
    if not placeholder_map:
        print("\nNo image placeholders found in markdown files.")
        print("The images have been extracted successfully though.")
        return
    
    # Step 3: Create or load mappings
    if args.apply_mappings and os.path.exists(args.mapping_file):
        # Load existing mappings
        with open(args.mapping_file, 'r') as f:
            config = json.load(f)
        
        # Use manual mappings if available, otherwise use suggestions
        mappings = config.get("manual_mappings", {})
        if not mappings:
            mappings = config.get("suggestions", {})
        
        if mappings:
            mapper.apply_mappings(mappings, backup=not args.no_backup)
            print("\nMapping complete!")
        else:
            print("No mappings found in configuration file.")
    else:
        # Generate suggestions and save configuration
        suggestions = mapper.suggest_mappings(placeholder_map)
        create_mapping_file(placeholder_map, suggestions, args.mapping_file)
        
        print("\nNext steps:")
        print(f"1. Review and edit the mapping file: {args.mapping_file}")
        print("2. Run again with --apply-mappings flag to apply the mappings")


if __name__ == "__main__":
    main()