#!/bin/bash
# Deploy site images to Cloudflare Pages CDN
# Usage: ./tools/deploy-images.sh <sitename>
# Deploys images/{sitename}/ + shared icons to https://{sitename}-images.pages.dev/

set -euo pipefail

SITE_NAME="${1:-}"
if [ -z "$SITE_NAME" ]; then
  echo "Usage: ./tools/deploy-images.sh <sitename>"
  exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
IMG_DIR="$PROJECT_DIR/images/$SITE_NAME"

if [ ! -d "$IMG_DIR" ]; then
  echo "ERROR: No images directory found at $IMG_DIR"
  exit 1
fi

# Copy shared icons (AZ logo, search) into the images dir for deployment
cp "$PROJECT_DIR/icons/astrazeneca-logo.svg" "$IMG_DIR/" 2>/dev/null || true
cp "$PROJECT_DIR/icons/search.svg" "$IMG_DIR/" 2>/dev/null || true

PROJECT_NAME="${SITE_NAME}-images"
echo "Deploying images for $SITE_NAME to Cloudflare Pages..."
echo "Project: $PROJECT_NAME"
echo "Source: $IMG_DIR"
echo ""

# Create Pages project if it doesn't exist (will silently fail if already exists)
npx wrangler pages project create "$PROJECT_NAME" --production-branch main 2>/dev/null || true

# Deploy
npx wrangler pages deploy "$IMG_DIR" --project-name "$PROJECT_NAME"

echo ""
echo "Images available at: https://${PROJECT_NAME}.pages.dev/"
