import time
import random
import streamlit as st
from bst import ContactBST, Contact

st.set_page_config(page_title="Contact Directory", page_icon="📇", layout="wide")

# Initialize BST and linear list in session state
if "bst" not in st.session_state:
    st.session_state.bst = ContactBST()
    st.session_state.linear_list = []  # Used for linear scan benchmark

    # Load initial test contacts
    initial_contacts = [
        Contact("Alice Smith", "555-0101", "alice@example.com"),
        Contact("Bob Jones", "555-0102", "bob@example.com"),
        Contact("Charlie Brown", "555-0103", "charlie@example.com"),
        Contact("Diana Prince", "555-0104", "diana@example.com"),
        Contact("Evan Wright", "555-0105", "evan@example.com"),
    ]
    for c in initial_contacts:
        st.session_state.bst.insert(c)
        st.session_state.linear_list.append(c)

st.title("📇 Contact Directory (BST Implementation)")
st.write("A Binary Search Tree contact directory featuring runtime performance benchmarks.")

# --- SIDEBAR (Actions) ---
st.sidebar.header("Manage Contacts")

# Add Contact
with st.sidebar.expander("➕ Add Contact", expanded=True):
    with st.form("add_contact_form"):
        name = st.text_input("Name")
        phone = st.text_input("Phone")
        email = st.text_input("Email")
        submit_add = st.form_submit_button("Add / Update")

        if submit_add and name:
            new_contact = Contact(name, phone, email)
            is_new = st.session_state.bst.insert(new_contact)
            
            # Update linear list as well
            st.session_state.linear_list = [c for c in st.session_state.linear_list if c.name.lower() != name.lower()]
            st.session_state.linear_list.append(new_contact)

            st.success(f"Contact '{name}' {'added' if is_new else 'updated'}!")
            st.rerun()

# Delete Contact
with st.sidebar.expander("🗑️ Delete Contact"):
    del_name = st.text_input("Name to delete")
    if st.button("Delete"):
        if del_name and st.session_state.bst.delete(del_name):
            st.session_state.linear_list = [
                c for c in st.session_state.linear_list if c.name.lower() != del_name.lower()
            ]
            st.success(f"Deleted '{del_name}'.")
            st.rerun()
        else:
            st.error("Contact not found.")

# Benchmark Tool: Bulk Add
st.sidebar.markdown("---")
st.sidebar.subheader("Benchmark Tools")
bulk_count = st.sidebar.number_input("Generate Dummy Contacts", min_value=10, max_value=50000, value=1000, step=500)
if st.sidebar.button("Add Bulk Contacts"):
    first_names = ["John", "Jane", "Alex", "Emily", "Chris", "Katie", "Michael", "Sarah"]
    last_names = ["Doe", "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller"]
    
    for i in range(bulk_count):
        fname = random.choice(first_names)
        lname = random.choice(last_names)
        cname = f"{fname} {lname} {random.randint(1, 99999)}"
        c = Contact(cname, f"555-{random.randint(1000,9999)}", f"{fname.lower()}@example.com")
        st.session_state.bst.insert(c)
        st.session_state.linear_list.append(c)
    
    st.sidebar.success(f"Added {bulk_count} contacts!")
    st.rerun()

# --- MAIN SECTION ---
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("🔍 Search & Performance Comparison")
    search_query = st.text_input("Search contact by name:", placeholder="Type name here...")

    if search_query:
        # 1. BST Search Timing
        start_bst = time.perf_counter_ns()
        bst_result = st.session_state.bst.search(search_query)
        end_bst = time.perf_counter_ns()
        bst_time = (end_bst - start_bst) / 1e6  # Convert to ms

        # 2. Linear Scan Timing
        start_linear = time.perf_counter_ns()
        linear_result = None
        for c in st.session_state.linear_list:
            if c.name.lower() == search_query.lower():
                linear_result = c
                break
        end_linear = time.perf_counter_ns()
        linear_time = (end_linear - start_linear) / 1e6  # Convert to ms

        # Display Search Result
        if bst_result:
            st.success(f"**Found:** {bst_result.name} | 📞 {bst_result.phone} | ✉️ {bst_result.email}")
        else:
            st.warning("Contact not found.")

        # Performance Comparison Metrics
        st.markdown("### ⏱️ Performance Metrics")
        m1, m2 = st.columns(2)
        m1.metric("BST Search (O(log n))", f"{bst_time:.4f} ms")
        m2.metric("Linear Search (O(n))", f"{linear_time:.4f} ms")

        if linear_time > 0 and bst_time > 0:
            speedup = linear_time / bst_time if bst_time > 0 else 1
            st.info(f"⚡ BST search was **{speedup:.1f}x faster** than linear search.")

with col2:
    st.subheader(f"📋 Ordered Contact List ({len(st.session_state.bst)} total)")
    ordered_contacts = st.session_state.bst.inorder()

    if ordered_contacts:
        table_data = [
            {"Name": c.name, "Phone": c.phone, "Email": c.email}
            for c in ordered_contacts
        ]
        st.dataframe(table_data, use_container_width=True, height=400)
    else:
        st.info("Directory is empty.")