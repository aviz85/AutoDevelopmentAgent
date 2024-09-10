from agent import AutoDevelopmentAgent

def main():
    print("Note: A new UI is available! Run 'streamlit run app.py' to use the web interface.")
    
    agent = AutoDevelopmentAgent()
    idea = input("Enter your idea for a software application: ")
    final_code = agent.process_user_idea(idea)
    
    print("\nFinal Code:")
    print(final_code)

    # Save the final code to a file
    with open("final_code.py", "w") as f:
        f.write(final_code)
    print("\nFinal code has been saved to 'final_code.py'")

if __name__ == "__main__":
    main()