RING = [
    [False, True, False, False, False, True],
    [True, False, True, False, False, False],
    [False, True, False, True, False, False],
    [False, False, True, False, True, False],
    [False, False, False, True, False, True],
    [True, False, False, False, True, False]
]

STAR = [
    [False, True, True, True, True, True],
    [True, False, False, False, False, False],
    [True, False, False, False, False, False],
    [True, False, False, False, False, False],
    [True, False, False, False, False, False],
    [True, False, False, False, False, False]
]

MESH = [
    [False, True, True, True, True, True],
    [True, False, True, True, True, True],
    [True, True, False, True, True, True],
    [True, True, True, False, True, True],
    [True, True, True, True, False, True],
    [True, True, True, True, True, False]
]


class Topology:

    def __init__(self, matrix):
        self.matrix = matrix
        self._validate()
        self.size = len(self.matrix)

    def print_matrix(self):
        print('\n'.join(['\t'.join([str(e) for e in row]) for row in self.matrix]))

    def row_disconnects(self, row_index):
        '''Returns a count of the topology disconnections for a row.

        :param row_index: Row to count disconnections in.
        :type row_index: int

        :returns: Count of disconnections in the specified row.
        :rtype: int
        '''
        disconnects = 0
        for element in self.matrix[row_index]:
            if not element:
                disconnects += 1

        return disconnects

    def col_disconnects(self, col_index):
        '''Returns a count of the topology disconnections for a column.

        :param col_index: Column to count disconnections in.
        :type col_index: int

        :returns: Count of disconnections in the specified column.
        :rtype: int
        '''
        disconnects = 0
        for row in self.matrix:
            if not row[col_index]:
                disconnects += 1

        return disconnects

    def is_ring(self):
        '''Returns the matrix's status as a ring.

        A topology is a ring iff each vertex connects to exactly two
        other vertices. Therefore, two connections should exist in each
        row of the adjacency matrix.

        :returns: True if the matrix is a ring, False otherwise.
        :rtype: bool
        '''
        row_index = 0
        col_index = 0

        while(row_index < self.size and col_index < self.size):
            row_disconnects = self.row_disconnects(row_index)
            col_disconnects = self.col_disconnects(col_index)

            if row_disconnects != self.size - 2:
                return False
            if col_disconnects != self.size - 2:
                return False

            row_index += 1
            col_index += 1

        return True

    def is_mesh(self):
        '''Returns the matrix's status as a fully connected mesh.

        A topology is a mesh iff each vertex connects to exactly n - 1
        other vertices, where n is the total number of vertices.
        Therefore, each row should have a single disconnection.

        :returns: True if the matrix is a mesh, False otherwise.
        :rtype: bool
        '''
        for row_index, row in enumerate(self.matrix):
            row_disconnects = self.row_disconnects(row_index)

            if row_disconnects != 1:
                return False

        return True

    def is_star(self):
        '''Returns the matrix's status as a star.

        A topology is a mesh iff each non-central vertex connects to
        exactly one other vertex, where n is the total number of
        vertices. The central vertex must connect to each of the n - 1
        other vertices. Therefore, the central vertex should have
        exactly one disconnection and each row should have exactly one
        connection.

        :returns: True if the matrix is a star, False otherwise.
        :rtype: bool
        '''
        is_central = False
        connections = 0

        for row_index, row in enumerate(self.matrix):
            row_disconnects = self.row_disconnects(row_index)
            if row_disconnects == 1 and not is_central:
                is_central = True
            elif row_disconnects == self.size - 1 and connections < self.size - 1:
                connections += 1
            else:
                return False

        return True

    def _validate(self):
        if len(self.matrix) != len(self.matrix[0]):
            raise Exception("Invalid matrix: must be nxn dimensions.")
        for row_index, row in enumerate(self.matrix):
            if row[row_index]:
                raise Exception("Invalid matrix: cannot contain loops.")


if __name__ == '__main__':
    topology = Topology(RING)
    print('matrix:')
    topology.print_matrix()
    print('ring:', topology.is_ring())
    print('mesh:', topology.is_mesh())
    print('star:', topology.is_star())
