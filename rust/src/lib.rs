use pyo3::{prelude::*};
use std::collections::{HashSet, VecDeque};

#[pyclass]
/// Tabu structure to store a set of forbidden moves with limited capacity.
pub struct TabuStructure {
    capacity: usize,
    queue: VecDeque<(i64, i64)>,
    tabu_set: HashSet<(i64, i64)>,
}

#[pymethods]
impl TabuStructure {
    #[new]
    /// Initializes the Tabu structure with a given maximum capacity.
    ///
    /// # Parameters
    /// - `capacity`: Maximum number of elements allowed in the tabu set.
    fn new(capacity: usize) -> Self {
        TabuStructure {
            capacity,
            queue: VecDeque::with_capacity(capacity),
            tabu_set: HashSet::with_capacity(capacity),
        }
    }

    /// Checks if the given element is in the tabu set (private method).
    ///
    /// # Parameters
    /// - `element`: Element to be checked.
    ///
    /// # Returns
    /// - `true` if the element is in the tabu set, `false` otherwise.
    fn check(&self, element: (i64, i64)) -> bool {
        self.tabu_set.contains(&element)
    }

    /// Public method to check if the element is in the tabu set.
    ///
    /// # Parameters
    /// - `element`: Element to find in the tabu set.
    ///
    /// # Returns
    /// - `true` if the element is found, `false` otherwise.
    pub fn find(&self, element: (i64, i64)) -> PyResult<bool>  {
        Ok(self.check(element))
    }

    /// Inserts a new element into the tabu set. If the element already exists, returns `false`
    /// without modifying the set. If the set exceeds its maximum size, the oldest element is removed.
    ///
    /// # Parameters
    /// - `element`: The element to add to the tabu set.
    pub fn insert(&mut self, element: (i64, i64)){
        if self.check(element) {
            return;
        }

        self.tabu_set.insert(element);
        self.queue.push_back(element);

        if self.queue.len() > self.capacity {
            if let Some(oldest) = self.queue.pop_front() {
                self.tabu_set.remove(&oldest);
            }
        }
    }
}

#[pymodule]
fn tabu_structure(module: &Bound<'_, PyModule>) -> PyResult<()> {
    module.add_class::<TabuStructure>()?;
    Ok(())
}