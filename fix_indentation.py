#!/usr/bin/env python

def fix_candidate_function(content):
    """Fix indentation in register_candidate function"""
    lines = content.split('\n')
    start_line = None
    end_line = None
    
    # Find the start and end of the function
    for i, line in enumerate(lines):
        if '@app.post("/register/candidate"' in line:
            start_line = i
        elif start_line is not None and '@app.get("/candidate/{candidate_id}"' in line:
            end_line = i
            break
            
    if start_line is None or end_line is None:
        print("Could not find register_candidate function")
        return content
        
    # Extract the function
    function_lines = lines[start_line:end_line]
    
    # Fix the indentation
    fixed_function = []
    fixed_function.append(function_lines[0])  # @app.post decorator
    fixed_function.append(function_lines[1])  # async def line
    fixed_function.append("    try:")  # try line with proper indent
    
    # Fix the indentation of the try block
    found_except = False
    for line in function_lines[3:]:
        if "except Exception as e:" in line:
            found_except = True
            fixed_function.append("    except Exception as e:")
            continue
            
        if found_except:
            if line.strip():  # If not an empty line
                fixed_function.append("        " + line.lstrip())
            else:
                fixed_function.append(line)
        else:
            if line.strip():  # If not an empty line
                fixed_function.append("        " + line.lstrip())
            else:
                fixed_function.append(line)
    
    # Replace the original function with the fixed one
    result = lines[:start_line] + fixed_function + lines[end_line:]
    return '\n'.join(result)

def fix_employer_function(content):
    """Fix indentation in register_employer function"""
    lines = content.split('\n')
    start_line = None
    end_line = None
    
    # Find the start and end of the function
    for i, line in enumerate(lines):
        if '@app.post("/register/employer"' in line:
            start_line = i
        elif start_line is not None and '@app.get("/employer/{employer_id}"' in line:
            end_line = i
            break
            
    if start_line is None or end_line is None:
        print("Could not find register_employer function")
        return content
        
    # Extract the function
    function_lines = lines[start_line:end_line]
    
    # Fix the indentation
    fixed_function = []
    fixed_function.append(function_lines[0])  # @app.post decorator
    fixed_function.append(function_lines[1])  # async def line
    fixed_function.append("    try:")  # try line with proper indent
    
    # Fix the indentation of the try block
    found_except = False
    for line in function_lines[3:]:
        if "except Exception as e:" in line:
            found_except = True
            fixed_function.append("    except Exception as e:")
            continue
            
        if found_except:
            if line.strip():  # If not an empty line
                fixed_function.append("        " + line.lstrip())
            else:
                fixed_function.append(line)
        else:
            if line.strip():  # If not an empty line
                fixed_function.append("        " + line.lstrip())
            else:
                fixed_function.append(line)
    
    # Replace the original function with the fixed one
    result = lines[:start_line] + fixed_function + lines[end_line:]
    return '\n'.join(result)

def main():
    try:
        # Read the original file
        with open('main.py', 'r') as f:
            content = f.read()
        
        # Fix the indentation in both functions
        content = fix_candidate_function(content)
        content = fix_employer_function(content)
        
        # Write the fixed content back to the file
        with open('main.py', 'w') as f:
            f.write(content)
            
        print("✓ Indentation fixed successfully!")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main() 