# --- Stage 1: The Builder Stage (for dependency caching) ---
FROM python:3.11-slim AS builder

WORKDIR /app

# Install dependencies into a dedicated layer
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


# --- Stage 2: The Final Production Stage ---
FROM python:3.11-slim

WORKDIR /app

# Create a non-root user for better security
RUN addgroup --system app && adduser --system --group app

# Copy the installed dependencies from the builder stage
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
# Also copy the executables like uvicorn
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy the application code
COPY . .

# Change ownership of the files to the non-root user
RUN chown -R app:app /app

# Switch to the non-root user
USER app

# Expose the port the application will run on
EXPOSE 8000

# The command to start the application server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]