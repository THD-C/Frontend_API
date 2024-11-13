import os
import subprocess

# Ścieżki do katalogów
proto_src_dir = './proto/Protocol/proto'
output_dir = 'src/grpc_generated'

# Tworzenie folderu wyjściowego, jeśli nie istnieje
os.makedirs(output_dir, exist_ok=True)

# Iteracja po wszystkich plikach .proto
for root, _, files in os.walk(proto_src_dir):
    for file in files:
        if file.endswith('.proto'):
            proto_file_path = os.path.join(root, file)
            print(f"Generating code for {proto_file_path}")

            # Uruchamianie protoc za pomocą subprocess
            result = subprocess.run([
                'python', '-m', 'grpc_tools.protoc',
                f'-I{proto_src_dir}',
                f'--python_out={output_dir}',
                f'--grpc_python_out={output_dir}',
                proto_file_path
            ], capture_output=True, text=True)

            # Sprawdzenie wyników i wyświetlenie komunikatów
            if result.returncode != 0:
                print(f"Error generating code for {proto_file_path}")
                print(result.stderr)
            else:
                print(f"Successfully generated code for {proto_file_path}")

print("Generation complete.")