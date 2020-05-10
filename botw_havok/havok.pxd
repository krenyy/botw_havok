cdef class Havok:
    cpdef public list files

    cpdef void deserialize(self)
    cpdef void serialize(self)

    cpdef void to_switch(self)
    cpdef void to_wiiu(self)

    cpdef str guess_extension(self)

    cpdef list as_dict(self)
